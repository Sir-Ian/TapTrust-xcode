import Foundation

struct CLI {
    static func run() {
        do {
            let raw = try NFCReader.tapAndGetPayload(attempts: 1)
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
            fputs("[error] \(error)\n", stderr)
        }
    }
}
