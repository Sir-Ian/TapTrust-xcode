import Foundation
#if canImport(CoreNFC)
import CoreNFC
#endif

public struct CoreNFCReader: Reader {
    public init() {}
    public mutating func open() throws {
        #if canImport(CoreNFC)
        // Real implementation would create NFCTagReaderSession
        throw NFCError.notSupported
        #endif
    }

    public func readMobileID() throws -> Data {
        #if canImport(CoreNFC)
        throw NFCError.notSupported
        #else
        let mock = URL(fileURLWithPath: "../examples/mock_cose_payload.cbor")
        return try Data(contentsOf: mock)
        #endif
    }

    public func close() {}
}

extension CoreNFCReader {
    public static let knownAIDs: [String: Data] = [
        "ISO18013": Data([0xD2,0x76,0x00,0x00,0x24,0x01,0x02,0x00]),
        "GET": Data([0xA0,0x00,0x00,0x03,0x96,0x54,0x00]),
        "Thales": Data([0xA0,0x00,0x00,0x02,0x47,0x10,0x01])
    ]
}
