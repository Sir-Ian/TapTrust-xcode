import pytest


from verifier.nfc.apdu import build_apdu, build_select_applet, try_select_aid
from verifier.nfc.reader import select_ef_com, read_binary_range


class FakeConn:
    def __init__(self, script):
        self.script = list(script)
        self.commands = []

    def transmit(self, apdu):
        self.commands.append(bytes(apdu))
        if not self.script:
            raise RuntimeError("no script")
        resp, sw1, sw2 = self.script.pop(0)
        return resp, sw1, sw2


def test_try_select_aid_success_after_failure():
    aids = [b"\x01\x01", b"\x02\x02"]
    conn = FakeConn([
        ([], 0x6A, 0x82),
        ([0x11, 0x22], 0x90, 0x00),
    ])
    aid, resp, sw1, sw2 = try_select_aid(conn, aids)
    assert aid == aids[1]
    assert resp == b"\x11\x22"
    assert sw1 == 0x90 and sw2 == 0x00
    assert conn.commands[0] == build_select_applet(aids[0])
    assert conn.commands[1] == build_select_applet(aids[1])


def test_try_select_aid_error_message():
    conn = FakeConn([(b"", 0x6A, 0x82)])
    with pytest.raises(RuntimeError) as exc:
        try_select_aid(conn, [b"\xAA"])
    assert "6a" in str(exc.value).lower()


def test_select_ef_com_builds_correct_apdu():
    conn = FakeConn([(b"", 0x90, 0x00)])
    resp, sw1, sw2 = select_ef_com(conn, 0x1234)
    assert sw1 == 0x90 and sw2 == 0x00
    assert conn.commands[0] == build_apdu(0x00, 0xA4, 0x02, 0x0C, b"\x12\x34")


def test_read_binary_range_multiple_blocks():
    conn = FakeConn([
        ([1, 2, 3], 0x90, 0x00),
        ([4, 5], 0x90, 0x00),
        ([], 0x6B, 0x00),
    ])
    data = read_binary_range(conn, block_size=3)
    assert data == b"\x01\x02\x03\x04\x05"
    assert conn.commands[0] == build_apdu(0x00, 0xB0, 0x00, 0x00, le=3)
    assert conn.commands[1] == build_apdu(0x00, 0xB0, 0x00, 0x03, le=3)
