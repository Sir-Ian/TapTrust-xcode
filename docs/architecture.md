# Architecture

This document describes the high-level architecture of the Mobile ID Verifier.

## Components
- **NFC Reader**: Interfaces with PCSC or vendor SDKs to communicate with mDLs.
- **APDU Service**: Handles APDU command exchange.
- **CBOR Decoder**: Parses CBOR payloads from the mDL.
- **COSE Handler**: Unwraps and verifies COSE signatures.
- **Signature Verifier**: Validates signatures using trusted anchors.

## Data Flow
Reader → APDU Service → CBOR Decoder → Signature Verifier

## Key Management
- Trust anchors are loaded from the `trust_anchors/` directory.
- Only whitelisted issuers in `settings.yaml` are trusted. See the example file
  in the repository root for the expected format.

## Extensibility
- Pluggable NFC reader layer.
- Modular decode and crypto components.
