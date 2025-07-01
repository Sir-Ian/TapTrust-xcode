import Foundation

enum NFCError: Error {
    case notSupported
    case cardNotPresent
    case tapFailed(String)
}

protocol Reader {
    mutating func open() throws
    func readMobileID() throws -> Data
    func close()
}
