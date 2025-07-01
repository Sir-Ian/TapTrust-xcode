from verifier.nfc.reader import tap_and_get_payload


def main():
    """Tap a phone and print the raw payload bytes."""
    print("Waiting for NFC tap...")
    try:
        data = tap_and_get_payload()
    except RuntimeError as e:
        print(f"Error: {e}")
        return
    print(f"Read {len(data)} bytes:\n{data.hex()}")


if __name__ == "__main__":
    main()
