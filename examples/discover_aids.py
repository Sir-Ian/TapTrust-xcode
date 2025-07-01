from smartcard.System import readers

from verifier.config import get_known_aids
from verifier.nfc.apdu import build_select_applet


def main():
    """Try each known mDL AID and print the response status words."""
    rdr_list = readers()
    if not rdr_list:
        print("No PC/SC readers found")
        return
    conn = rdr_list[0].createConnection()
    conn.connect()

    aids = get_known_aids()
    for name, aid in aids.items():
        apdu = build_select_applet(aid)
        _, sw1, sw2 = conn.transmit(list(apdu))
        print(f"{name}: SW1={hex(sw1)} SW2={hex(sw2)}")


if __name__ == "__main__":
    main()
