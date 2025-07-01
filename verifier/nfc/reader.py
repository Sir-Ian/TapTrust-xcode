"""NFC reader helpers."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Callable

import logging
from verifier.config import get_known_aids, get_ef_com_file_id

from .apdu import build_apdu, is_success, try_select_aid

try:  # Optional pyscard dependency
    from smartcard.CardRequest import CardRequest
    from smartcard.CardType import AnyCardType
    from smartcard.System import readers
    from smartcard.scard import SCARD_PROTOCOL_T1
    from smartcard.Exceptions import (
        CardRequestTimeoutException,
        NoReadersException,
        CardConnectionException,
        NoCardException,
    )
except Exception:  # pragma: no cover - allow import to fail for tests
    CardRequest = AnyCardType = None  # type: ignore

    def readers():  # type: ignore
        raise ImportError("pyscard is required for NFC operations")

    SCARD_PROTOCOL_T1 = 0

    class CardRequestTimeoutException(Exception):
        pass

    class NoReadersException(Exception):
        pass

    class CardConnectionException(Exception):
        pass

    class NoCardException(Exception):
        pass


logger = logging.getLogger(__name__)


# Environment variable to force mock payload
MOCK_ENV = "TAPTRUST_USE_MOCK"


def _read_mock_payload() -> bytes:
    """Return the bundled example (mock) CBOR/COSE payload."""
    mock_file = (
        Path(__file__).resolve().parents[2]
        / "examples"
        / "mock_cose_payload.cbor"
    )
    return mock_file.read_bytes()


def _get_pcsc_reader():
    """Return the first available PC/SC reader, preferring ACR1252U."""
    rdr_list = readers()
    if not rdr_list:
        raise RuntimeError(
            "No PC/SC readers found. Is the ACR1252U connected and "
            "drivers installed?"
        )

    for rdr in rdr_list:
        if "ACR1252" in str(rdr):
            logger.debug("using reader %s", rdr)
            return rdr

    logger.debug("using reader %s", rdr_list[0])
    return rdr_list[0]


def select_ef_com(conn, file_id: int = 0x0015) -> tuple[list[int], int, int]:
    """SELECT the EF.Com file by its 2-byte identifier."""
    if not 0 <= file_id <= 0xFFFF:
        raise ValueError("file_id must be in range 0..65535")

    fid = file_id.to_bytes(2, "big")
    apdu = build_apdu(0x00, 0xA4, 0x02, 0x0C, data=fid)
    return conn.transmit(list(apdu))


def read_binary_range(conn, start: int = 0, block_size: int = 0xFF) -> bytes:
    """READ BINARY in chunks until the selected file is exhausted."""
    full = bytearray()
    offset = start
    while True:
        p1 = (offset >> 8) & 0xFF
        p2 = offset & 0xFF
        apdu = build_apdu(0x00, 0xB0, p1, p2, le=block_size)
        resp, sw1, sw2 = conn.transmit(list(apdu))
        if not is_success(sw1, sw2):
            break
        full.extend(resp)
        offset += len(resp)
        if len(resp) < block_size:
            break
    return bytes(full)


def select_mdl_applet(conn) -> bytes:
    """Select an mDL applet using configured AIDs."""
    aids = list(get_known_aids().values())
    try:
        aid, _, sw1, sw2 = try_select_aid(conn, aids)
        logger.debug("selected AID %s (%s %s)", aid.hex(), hex(sw1), hex(sw2))
        return aid
    except RuntimeError as exc:
        raise RuntimeError(f"AID selection failed: {exc}") from None


def open_ef_com(conn, file_id: int | None = None) -> None:
    """Select the EF.Com file specified in settings or ``file_id``."""
    if file_id is None:
        file_id = get_ef_com_file_id()
    _, sw1, sw2 = select_ef_com(conn, file_id=file_id)
    if not is_success(sw1, sw2):
        raise RuntimeError(f"SELECT EF.Com failed: {hex(sw1)} {hex(sw2)}")
    logger.debug("selected EF.Com file %s", hex(file_id))


def read_cose_payload(conn) -> bytes:
    """Read the full COSE payload from the currently selected file."""
    data = read_binary_range(conn)
    logger.debug("read %d bytes", len(data))
    return data


def tap_and_get_payload(
    timeout: int = 10,
    *,
    ef_com_file_id: int | None = None,
    attempts: int = 1,
    progress: Callable[[int], None] | None = None,
) -> bytes:
    """Read a COSE payload from a tapped mobile ID.

    Parameters
    ----------
    timeout
        Seconds to wait for a tap.
    ef_com_file_id
        Optional file identifier for EF.Com. If ``None`` the value from
        the settings file is used.
    attempts
        How many tap attempts before giving up.
    progress
        Optional callback `progress(attempt)` before each try.

    Returns
    -------
    bytes
        The raw CBOR‐encoded COSE payload.
    """
    # 0) Mock fallback
    if os.getenv(MOCK_ENV):
        return _read_mock_payload()

    reader = _get_pcsc_reader()

    attempt = 0
    while attempt < attempts:
        if progress:
            progress(attempt)
        logger.debug("tap attempt %d", attempt + 1)

        try:
            with CardRequest(
                cardType=AnyCardType(), timeout=timeout, readers=[reader]
            ) as req:
                with req.waitforcard() as svc:
                    conn = svc.connection
                    conn.connect(protocol=SCARD_PROTOCOL_T1)
                    logger.debug("ATR %s", bytes(conn.getATR()).hex())

                    # 1) Select an mDL applet (try all known AIDs)
                    select_mdl_applet(conn)

                    # 2) Select EF.Com
                    open_ef_com(conn, file_id=ef_com_file_id)

                    # 3) Read the full COSE payload
                    return read_cose_payload(conn)

        except NoReadersException:
            raise RuntimeError(
                "No PC/SC readers found. "
                "Is the ACR1252U connected and drivers installed?"
            ) from None
        except (CardConnectionException, NoCardException):
            attempt += 1
            if attempt >= attempts:
                raise RuntimeError(
                    "NFC device removed during operation"
                ) from None
            # else: retry

        except CardRequestTimeoutException:
            attempt += 1
            if attempt >= attempts:
                raise RuntimeError("No NFC device detected") from None
            # else: retry

        except Exception as exc:  # pragma: no cover
            raise RuntimeError(f"NFC read failed: {exc}") from None

    # Shouldn’t be reached
    raise RuntimeError("Failed to read payload after retries")


if __name__ == "__main__":  # pragma: no cover
    """Smoke-test: run ``tap_and_get_payload`` standalone and print hex."""
    try:
        raw = tap_and_get_payload(
            attempts=3, progress=lambda i: print(f"Attempt {i+1}")
        )
    except RuntimeError as e:
        print(f"[error] {e}")
    else:
        print(raw.hex())
