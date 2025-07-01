import pytest

from verifier.decode.cbor import decode_payload


def test_decode_payload_returns_expected_keys(tmp_path):
    """CBOR payload bytes should decode into a dictionary"""
    payload = {"foo": "bar", "num": 123}
    try:
        import cbor2
    except ImportError:
        pytest.skip("cbor2 not installed")

    raw = cbor2.dumps(payload)

    result = decode_payload(raw)
    assert isinstance(result, dict)
    assert set(result.keys()) == set(payload.keys())
