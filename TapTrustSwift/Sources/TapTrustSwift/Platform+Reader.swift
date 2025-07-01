#if canImport(PCSC)
import PCSC
public typealias SystemReader = PCSCReader
#elseif canImport(CoreNFC)
import CoreNFC
public typealias SystemReader = CoreNFCReader
#else
import Foundation
public struct DummyReader: Reader {
    public init() {}
    public mutating func open() throws { throw NFCError.notSupported }
    public func readMobileID() throws -> Data { throw NFCError.notSupported }
    public func close() {}
}
public typealias SystemReader = DummyReader
#endif
