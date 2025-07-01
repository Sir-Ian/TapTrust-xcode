# Swift Migration Guide

This document highlights key differences between the existing Python verifier and a potential Swift implementation.

## Architecture Changes
- **NFC stack**: Python relies on `pyscard`/`nfcpy` over PC/SC. Swift would use `CoreNFC` to communicate with the secure element on iOS devices.
- **Cryptography**: Python uses `pycose` and `cryptography`. In Swift, `CryptoKit` or a compatible COSE library would handle signatures and encryption.
- **Data decoding**: `cbor2` decodes CBOR in Python. Swift should use a package such as `SwiftCBOR` for CBOR and a COSE helper (e.g. `SwiftCOSE`).
- **CLI vs App**: The Python tool is CLI-oriented. A Swift port would likely be part of an iOS app with its own UI and permission flow.

## Required Swift Packages
- `CoreNFC` – NFC reader access.
- `CryptoKit` – hashing and ECDSA verification.
- A CBOR library such as `SwiftCBOR`.
- A COSE library (for example `SwiftCOSE`).

## Platform Limitations
- `CoreNFC` is available only on iPhone models with NFC hardware and requires iOS 13 or later. iPad support is limited.
- Accessing the secure element requires user permission and entitlement configuration in Xcode.
- App Store deployment may require explanation of NFC usage in the privacy settings.

