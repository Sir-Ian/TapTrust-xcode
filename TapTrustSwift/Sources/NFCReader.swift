import Foundation
#if canImport(CoreNFC)
import CoreNFC
#endif

enum NFCError: Error {
    case notSupported
    case tapFailed(String)
}

struct NFCReader {
    // Placeholder AIDs matching verifier/nfc/apdu.py
    static let knownAIDs: [String: Data] = [
        "ISO18013": Data([0xD2,0x76,0x00,0x00,0x24,0x01,0x02,0x00]),
        "GET": Data([0xA0,0x00,0x00,0x03,0x96,0x54,0x00]),
        "Thales": Data([0xA0,0x00,0x00,0x02,0x47,0x10,0x01])
    ]

    static func tapAndGetPayload(timeout: TimeInterval = 10, attempts: Int = 1) throws -> Data {
        #if canImport(CoreNFC)
        // This is a simplified placeholder implementation.
        // A real implementation would use `NFCTagReaderSession` to poll for tags,
        // SELECT the mDL applet, then read EF.Com.
        throw NFCError.notSupported // real NFC not available in this environment
        #else
        // For testing on non-iOS platforms, load the bundled mock payload
        let mock = URL(fileURLWithPath: "../examples/mock_cose_payload.cbor")
        return try Data(contentsOf: mock)
        #endif
    }
}
