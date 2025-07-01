import Foundation
import SwiftCBOR

struct CBORCOSE {
    static func decodePayload(raw: Data) throws -> [String: Any] {
        // Attempt COSE decoding first
        if let dict = try? unwrapCOSE(coseBytes: raw) {
            return dict
        }
        // Fallback to plain CBOR
        guard case let .map(obj) = try CBOR.decode(raw) else {
            throw NSError(domain: "CBOR", code: 1, userInfo: [NSLocalizedDescriptionKey: "Top-level object is not a map"])
        }
        return objToDict(obj)
    }

    private static func unwrapCOSE(coseBytes: Data) throws -> [String: Any]? {
        // This is a stub that roughly follows verifier/decode/cose.py
        // Parsing a full COSE_Sign1 structure would require a full COSE library.
        // For this example we only extract the payload assuming structure [h,a,p,s].
        guard let arr = try? CBOR.decode(coseBytes) else {
            return nil
        }
        guard case let .array(items) = arr, items.count >= 4 else { return nil }
        let payload = items[2]
        guard case let .byteString(data) = payload else { return nil }
        guard case let .map(obj) = try CBOR.decode(data) else { return nil }
        var dict = objToDict(obj)
        if case let .byteString(sig) = items[3] {
            dict["signature"] = Data(sig)
        }
        return dict
    }

    private static func objToDict(_ map: [CBOR: CBOR]) -> [String: Any] {
        var out: [String: Any] = [:]
        for (k, v) in map {
            guard case let .utf8String(key) = k else { continue }
            out[key] = v.swiftValue
        }
        return out
    }
}

private extension CBOR {
    var swiftValue: Any {
        switch self {
        case let .utf8String(s):
            return s
        case let .byteString(b):
            return Data(b)
        case let .unsignedInt(i):
            return Int(i)
        case let .negativeInt(i):
            return -Int(i) - 1
        case let .map(m):
            return m.mapValues { $0.swiftValue }
        case let .array(a):
            return a.map { $0.swiftValue }
        default:
            return String(describing: self)
        }
    }
}
