"""Tests for APDU helpers."""

import pytest
from verifier.nfc.apdu import (
    build_apdu,
    build_select_applet,
    parse_response,
    is_success,
)


def test_build_apdu_basic():
    apdu = build_apdu(0x00, 0xA4, 0x04, 0x00)
    assert apdu == b"\x00\xA4\x04\x00"


def test_build_apdu_with_data_and_le():
    apdu = build_apdu(0x80, 0xCA, 0x00, 0x00, data=b"\x01\x02", le=0x10)
    assert apdu == b"\x80\xCA\x00\x00\x02\x01\x02\x10"


def test_build_select_applet():
    aid = bytes.fromhex("A0000002471001")
    apdu = build_select_applet(aid)
    expected = b"\x00\xA4\x04\x00" + bytes([len(aid)]) + aid
    assert apdu == expected


def test_parse_response_and_is_success():
    resp = b"\xDE\xAD\xBE\xEF\x90\x00"
    data, sw1, sw2 = parse_response(resp)
    assert data == b"\xDE\xAD\xBE\xEF"
    assert sw1 == 0x90 and sw2 == 0x00
    assert is_success(sw1, sw2) is True


def test_parse_response_too_short():
    with pytest.raises(ValueError):
        parse_response(b"\x90")
