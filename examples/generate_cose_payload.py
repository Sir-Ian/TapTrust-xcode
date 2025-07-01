# examples/generate_cose_payload.py

"""
Generate a minimal COSE_Sign1 file for testing.
This signs a CBOR‐encoded dict {"doc":{…}} with a temporary EC2 key.
"""

from pathlib import Path

import cbor2
from pycose.messages import Sign1Message
from pycose.algorithms import Es256
from pycose.keys.ec2 import EC2Key
from pycose.keys.curves import P256


def main():
    # 1. Create sample payload dict
    payload_dict = {
        "doc": {
            "first_name": "Alice",
            "last_name": "Example",
            "dob": "1995-07-20",
            "issuing_state": "OH",
            "expiry": "2029-07-20"
        }
    }
    # 2. CBOR‐encode the payload dict
    payload_cbor = cbor2.dumps(payload_dict)

    # 3. Generate a new EC2 key (P‐256) for signing
    key = EC2Key.generate_key(P256)

    # 4. Create and sign a COSE_Sign1 message
    msg = Sign1Message(phdr={"alg": Es256}, payload=payload_cbor)
    msg.key = key
    msg.compute_signature()
    signed = msg.encode()  # CBOR‐encoded COSE_Sign1 structure

    # 6. Write to examples/mock_cose.cbor
    out = Path("examples") / "mock_cose_payload.cbor"
    out.write_bytes(signed)
    print(f"✅ Wrote COSE payload to {out.resolve()}")


if __name__ == "__main__":
    main()
