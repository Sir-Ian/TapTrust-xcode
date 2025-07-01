import Foundation
import SwiftCBOR

public struct CBORCOSE {
    public static func decodePayload(raw: Data) throws -> [String: Any] {
        // Attempt COSE decoding first
        if let dict = try? unwrapCOSE(coseBytes: raw) {
            return dict
        }
        // Fallback to plain CBOR
        guard case let .map(obj) = try CBOR.decode([UInt8](raw)) else {
            throw NSError(
                domain: "CBOR",
                code: 1,
                userInfo: [NSLocalizedDescriptionKey: "Top-level object is not a map"]
            )
        }
        return objToDict(obj)
    }

    private static func unwrapCOSE(coseBytes: Data) throws -> [String: Any]? {
        // Stub following verifier/decode/cose.py: we only extract payload from [h,a,p,s]
        guard let arr = try? CBOR.decode([UInt8](coseBytes)),
              case let .array(items) = arr,
              items.count >= 4
        else {
            return nil
        }
        let payload = items[2]
        guard case let .byteString(data) = payload,
              case let .map(obj) = try CBOR.decode([UInt8](data))
        else {
            return nil
        }

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
