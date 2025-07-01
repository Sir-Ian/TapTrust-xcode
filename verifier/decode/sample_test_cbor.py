# tests/test_cbor.py

import pytest
from verifier.decode.cbor import decode_payload


def test_decode_payload_returns_expected_keys(tmp_path):
    # Write a tiny CBOR payload to a temp file
    payload = {"foo": "bar", "num": 123}
    raw = b""
    try:
        import cbor2
    except ImportError:
        pytest.skip("cbor2 not installed")
    raw = cbor2.dumps(payload)

    result = decode_payload(raw)
    assert isinstance(result, dict)
    assert result["foo"] == "bar"
    assert result["num"] == 123
