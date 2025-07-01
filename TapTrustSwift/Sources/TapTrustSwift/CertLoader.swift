import Foundation

struct CertLoader {
    static func loadKey(for issuer: String) -> Data? {
        // Look for PEM file in ../trust_anchors/<ISSUER>.pem
        let path = URL(fileURLWithPath: "../trust_anchors/\(issuer).pem")
        guard let pemData = try? Data(contentsOf: path) else { return nil }
        return pemToKey(pem: pemData)
    }

    private static func pemToKey(pem: Data) -> Data? {
        guard let pemString = String(data: pem, encoding: .utf8) else { return nil }
        let lines = pemString.split(separator: "\n").filter { !$0.hasPrefix("---") }
        let base64 = lines.joined()
        return Data(base64Encoded: base64)
    }
}
