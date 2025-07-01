import Foundation

public enum NFCError: Error {
    case notSupported
    case cardNotPresent
    case tapFailed(String)
}

public protocol Reader {
    mutating func open() throws
    func readMobileID() throws -> Data
    func close()
}
