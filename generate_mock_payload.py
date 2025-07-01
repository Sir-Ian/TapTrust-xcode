# generate_mock_payload.py

from pathlib import Path

import cbor2


def main():
    """
    Generate a simple CBOR file at examples/mock_payload.cbor.
    """

    example_doc = {
        "doc": {
            "first_name": "Alice",
            "last_name": "Example",
            "dob": "1995-07-20",
            "issuing_state": "OH",
            "expiry": "2029-07-20"
        },
        # Placeholder bytes for the signature field
        "signature": b"MOCK_SIGNATURE"
    }

    # Encode the dict as CBOR
    encoded = cbor2.dumps(example_doc)

    # Ensure examples/ directory exists
    examples_dir = Path("examples")
    examples_dir.mkdir(parents=True, exist_ok=True)

    # Write the CBOR bytes to examples/mock_payload.cbor
    out = examples_dir / "mock_payload.cbor"
    out.write_bytes(encoded)

    print(f"✅ Wrote mock CBOR to {out.resolve()}")


if __name__ == "__main__":
    main()
