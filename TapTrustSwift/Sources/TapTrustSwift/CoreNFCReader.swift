import Foundation
#if canImport(CoreNFC)
import CoreNFC
#endif

public struct CoreNFCReader: Reader {
    private static let mockPayload: URL = {
        var url = URL(fileURLWithPath: #file)
        url.deleteLastPathComponent()
        url.deleteLastPathComponent()
        return url.appendingPathComponent("examples/mock_cose_payload.cbor")
    }()
    
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
        return try Data(contentsOf: Self.mockPayload)
        #endif
    }
    
    public func close() {}
}

extension CoreNFCReader {
    public static let knownAIDs: [String: Data] = [
        "ISO18013": Data([0xD2, 0x76, 0x00, 0x00, 0x24, 0x01, 0x02, 0x00]),
        "GET":       Data([0xA0, 0x00, 0x00, 0x03, 0x96, 0x54, 0x00]),
        "Thales":    Data([0xA0, 0x00, 0x00, 0x02, 0x47, 0x10, 0x01])
    ]
}
