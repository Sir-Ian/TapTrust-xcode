# verifier/nfc/apdu.py

"""Utility helpers for constructing and parsing APDU commands."""

from __future__ import annotations

from typing import Sequence, Tuple


def build_apdu(
    cla: int,
    ins: int,
    p1: int,
    p2: int,
    data: bytes = b"",
    le: int | None = None,
) -> bytes:
    """Build a simple APDU command.

    Parameters
    ----------
    cla, ins, p1, p2:
        Header bytes of the APDU.
    data:
        Optional command data. ``Lc`` is inserted automatically when present.
    le:
        Expected length of the response. ``Le`` is appended when supplied.

    Returns
    -------
    bytes
        Raw APDU ready to send to the card/reader.
    """

    if not all(0 <= x <= 0xFF for x in (cla, ins, p1, p2)):
        raise ValueError("APDU header bytes must be in range 0..255")

    if len(data) > 255:
        raise ValueError("APDU data field too long")

    parts = [bytes([cla, ins, p1, p2])]
    if data:
        parts.append(bytes([len(data)]))
        parts.append(data)
    if le is not None:
        if not 0 <= le <= 0xFF:
            raise ValueError("Le must be in range 0..255")
        parts.append(bytes([le]))

    return b"".join(parts)


def build_select_applet(aid: bytes) -> bytes:
    """Return a ``SELECT`` command APDU for ``aid``."""

    if not aid:
        raise ValueError("aid is empty")
    if len(aid) > 255:
        raise ValueError("aid too long")
    return build_apdu(0x00, 0xA4, 0x04, 0x00, aid)


def parse_response(resp: bytes) -> Tuple[bytes, int, int]:
    """Split APDU response ``resp`` into payload and status words."""

    if len(resp) < 2:
        raise ValueError("response too short")

    data = resp[:-2]
    sw1, sw2 = resp[-2], resp[-1]
    return data, sw1, sw2


def is_success(sw1: int, sw2: int) -> bool:
    """Return ``True`` if status words indicate success (``0x9000``)."""

    return sw1 == 0x90 and sw2 == 0x00


def try_select_aid(conn, aids: Sequence[bytes]):
    """Attempt to ``SELECT`` each AID in ``aids``.

    Parameters
    ----------
    conn:
        pyscard connection object used to transmit APDUs.
    aids:
        Sequence of candidate AIDs.

    Returns
    -------
    tuple
        ``(aid, resp, sw1, sw2)`` of the first successful selection.

    Raises
    ------
    RuntimeError
        If all selections fail. The message aggregates status words
        for each attempted AID.
    """

    statuses = []
    for aid in aids:
        apdu = build_select_applet(aid)
        resp, sw1, sw2 = conn.transmit(list(apdu))
        if is_success(sw1, sw2):
            return aid, bytes(resp), sw1, sw2
        statuses.append((aid.hex(), sw1, sw2))

    status_str = ", ".join(
        f"{a}: {hex(sw1)} {hex(sw2)}" for a, sw1, sw2 in statuses
    )
    raise RuntimeError(f"SELECT AID failed for all known AIDs [{status_str}]")
