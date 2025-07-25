#if os(macOS)
import Foundation
import PCSC

public struct PCSCReader: Reader {
    private static let mockPayload: URL = {
        var url = URL(fileURLWithPath: #file)
        url.deleteLastPathComponent()
        url.deleteLastPathComponent()
        return url.appendingPathComponent("examples/mock_cose_payload.cbor")
    }()

    private var context: SCardContext?
    private var handle: SCardHandle?
    private var proto: SCardProtocol = .undefined

    public init() {}
    public mutating func open() throws {
        context = try SCardEstablishContext(.system)
        guard let ctx = context else { throw NFCError.tapFailed("Context") }
        let readers = try SCardListReaders(ctx)
        guard let name = readers.first else {
            throw NFCError.tapFailed("No reader")
        }
        let connection = try SCardConnect(ctx, name, .shared, [.t1])
        handle = connection.phCard
        proto = connection.pdwActiveProtocol
    }

    public func readMobileID() throws -> Data {
        guard handle != nil else { throw NFCError.cardNotPresent }
        // Real APDU exchange omitted. Use mock data for now.
        return try Data(contentsOf: Self.mockPayload)
    }

    public func close() {
        if let h = handle { try? SCardDisconnect(h, .leave) }
        if let ctx = context { try? SCardReleaseContext(ctx) }
    }
}
#endif
