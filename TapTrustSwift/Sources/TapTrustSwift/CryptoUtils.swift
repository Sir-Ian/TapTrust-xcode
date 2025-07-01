import Foundation
#if canImport(CryptoKit)
import CryptoKit
#else
import Crypto
#endif
import SwiftCBOR

public struct CryptoUtils {
    public static func verifySignature(parsed: [String: Any]) -> Bool {
        guard let doc = parsed["doc"] as? [String: Any],
              let sigData = parsed["signature"] as? Data,
              let issuer = (doc["issuing_state"] as? String)?.uppercased() else {
            return false
        }
        guard let key = CertLoader.loadKey(for: issuer) else {
            return false
        }
        guard let cborBytes = try? CBOR.encodeAny(doc) else {
            return false
        }
        do {
            let pub = try P256.Signing.PublicKey(x963Representation: key)
            let signature = try P256.Signing.ECDSASignature(rawRepresentation: sigData)
            return pub.isValidSignature(signature, for: Data(cborBytes))
        } catch {
            return false
        }
    }

    public static func hkdfSHA256(inputKey: Data, salt: Data?, info: Data, outputLength: Int) -> Data {
        let key = SymmetricKey(data: inputKey)
        let saltKey: Data = salt ?? Data()
        let derived = HKDF<SHA256>.deriveKey(inputKeyMaterial: key, salt: saltKey, info: info, outputByteCount: outputLength)
        return Data(derived.withUnsafeBytes { Data($0) })
    }

    public static func aesGCM(key: Data) -> AES.GCM.SealedBox? {
        // Placeholder to show AES.GCM usage
        nil
    }
}
