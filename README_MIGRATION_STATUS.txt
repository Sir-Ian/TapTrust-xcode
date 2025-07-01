All core functionality and tests have been ported to Swift. The following Python files are now redundant and can be deleted:

- verifier/cli.py
- verifier/decode/cbor.py
- verifier/decode/cose.py
- verifier/nfc/reader.py
- verifier/nfc/apdu.py
- examples/read_raw_payload.py
- examples/discover_aids.py
- examples/generate_mock_payload.py
- examples/generate_cose_payload.py
- tests/test_apdu.py
- tests/test_reader_helpers.py
- tests/test_cbor.py
- tests/test_verify.py
- tests/test_secure_channel.py
- verifier/decode/test_decode_cbor.py
- verifier/decode/sample_test_cbor.py
- generate_mock_payload.py

If you need to generate new mock payloads, use the Swift utility in TapTrustSwift/MockPayloadGenerator.swift.
