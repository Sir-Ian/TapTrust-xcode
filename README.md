# TapTrust
Making the Ohio mobile id work in ways that are useful (i hope lol)

TapTrust is a verifier for mobile driver’s licences (mDLs).
Built around ISO 18013-5, it speaks NFC/APDU, decodes CBOR/COSE, and validates signatures against state trust anchors.
Think “⚡ Tap-your-phone” age checks for bars today, cops tomorrow.
CLI first, pluggable into any POS or patrol tablet next.

# TapTrust

> *Tap-to-trust digital IDs.* Verify Apple/Google Wallet driver’s licences in <1 sec.

## Why ?

* **Universal** – Implements ISO/IEC 18013-5, works across IDEMIA, GET Group, Thales.
* **Privacy-smart** – Zero-retention; we discard payloads right after signature check.
* **Pluggable** – Clean driver layer → swap in any NFC reader without breaking logic.

## Architecture (one-screen view)

Reader ─┬─> APDU Service ─┬─> CBOR Decoder ─┬─> Signature Verifier
│ │ │
│<── error codes ──┘ │
└─<── verdict/fields <─────────────────┘

Key management

Place issuing-state root certs in `trust_anchors/`.
Edit `settings.yaml` to whitelist which issuers you trust. A sample file is
provided in the repository root.
(No real DMV keys? Run make dev-ca to generate mocks.)

### Using a real NFC reader

TapTrust will attempt to read a mobile ID from the first PC/SC compatible NFC
reader (for example the ACR1252U).  Set the environment variable
`TAPTRUST_USE_MOCK=1` to force the CLI to use the bundled example payload
instead of real hardware.  The `pyscard` package is required for reader access
and is installed automatically via Poetry. Installation of `pyscard` also
requires the PC/SC development headers. On macOS install them with
`brew install pcsc-lite`, or on Linux run `apt-get install libpcsclite-dev`.

Behind the scenes the CLI enumerates PC/SC readers with
``smartcard.System.readers()`` and prefers the ``ACR1252U`` if present.
Connections are opened with protocol ``T=1`` and the card's ATR is logged for
debugging.  If no reader is found a helpful message prompts you to verify the
USB connection and drivers.

#### Read raw NFC payload

If you just want to see what the reader returns, run the example script:

```bash
poetry run python examples/read_raw_payload.py
```

Tap your phone when prompted and the raw bytes will be printed to the
terminal.

#### Discover available AIDs

If ``SELECT`` fails with ``6A82`` you may be using the wrong AID. The
``examples/discover_aids.py`` helper tries a few known vendor AIDs and prints
their responses:

```bash
poetry run python examples/discover_aids.py
```


Overview and Goals

Apple’s implementation of mobile driver’s licenses (mDL) in Wallet follows the ISO/IEC 18013‑5 standard for device retrieval – meaning an iPhone can act as a secure NFC credential that any compliant reader can scan

. Our goal is to extend the TapTrust CLI (a Python-based verifier) to read an Ohio mDL from an iPhone via an ACR1252U NFC reader, extract all identity fields, and verify authenticity offline. The high-level process will be:
NFC Handshake (Device Engagement): Establish a secure session by exchanging cryptographic keys with the iPhone’s Secure Element (per ISO 18013‑5). This ensures data is encrypted and bound to the device (preventing cloning)

.
APDU Data Exchange: Use ISO 7816-4 APDU commands over PC/SC to request the mDL data. This involves selecting the mDL application and sending a Reader Request that specifies which data elements to retrieve (e.g. name, DOB, etc.), then receiving the mDL Response from the phone
mobiledl-e5018.web.app
.
Decrypt and Decode: Decrypt the response using session keys from the handshake, yielding a COSE_Sign1-wrapped CBOR data structure containing the requested identity fields and a digital signature
mobiledl-e5018.web.app
.
Signature Verification: Use the Ohio issuer’s root certificate to validate the COSE signature (ensuring the data was signed by Ohio’s DMV and hasn’t been tampered)

. All data elements are individually protected by the signature to allow selective disclosure with privacy

.
Data Extraction: Parse the CBOR structure to extract all available fields (name, birth date, expiration date, issuing state, etc.) and return them via the CLI. We will design the solution to be extensible for other states and issuer configurations in the future.
Throughout this plan, we’ll detail each step with best practices (e.g. handling APDU lengths, user consent timing) and debugging tips. The implementation will leverage TapTrust’s existing NFC communication, CBOR decoding, and COSE signature verification capabilities, using Python libraries (e.g. pyscard for PC/SC and cryptography or COSE libraries for signature checks).


🛣️ Roadmap

Phase	Goal	ETA
0.1	CLI verifier + mock keys	2025-07
0.2	Real cert chain (AZ or MD pilot)	2025-Q4
0.3	Electron GUI / SDK for POS	2026-Q1
🤝 Contributing

PRs welcome! See docs/CONTRIBUTING.md for setup, lint, test, and CI rules.

📜 License

MIT
