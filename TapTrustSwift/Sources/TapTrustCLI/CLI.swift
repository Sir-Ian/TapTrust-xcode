import Foundation
import TapTrustSwift

struct CLI {
    static func run() {
        var reader = SystemReader()
        do {
            try reader.open()
            let raw = try reader.readMobileID()
            reader.close()
            let parsed = try CBORCOSE.decodePayload(raw: raw)
            let valid = CryptoUtils.verifySignature(parsed: parsed)
            var output: [String: Any] = ["valid": valid]
            if let doc = parsed["doc"] as? [String: Any] {
                output["fields"] = doc
            } else {
                output["fields"] = parsed
            }
            let json = try JSONSerialization.data(withJSONObject: output, options: .prettyPrinted)
            if let str = String(data: json, encoding: .utf8) {
                print(str)
            }
        } catch {
            FileHandle.standardError.write(Data("[error] \(error)\n".utf8))
        }
    }
}
