import Foundation
import SwiftCBOR
import CryptoKit

public struct MockPayloadGenerator {
    public static func generateMockCOSEPayload() throws -> Data {
        // 1. Create sample payload dict
        let doc: [String: Any] = [
            "first_name": "Alice",
            "last_name": "Example",
            "dob": "1995-07-20",
            "issuing_state": "OH",
            "expiry": "2029-07-20"
        ]
        let payloadDict: [String: Any] = ["doc": doc]
        let payloadCBOR = try CBOR.encodeAny(payloadDict)
        let payloadData = Data(payloadCBOR)

        // 2. Generate a new EC key for signing (P-256)
        let privateKey = P256.Signing.PrivateKey()
        let publicKey = privateKey.publicKey

        // 3. Create COSE_Sign1 structure: [protected, unprotected, payload, signature]
        let protected: [UInt8] = [] // No protected headers for mock
        let unprotected: [UInt8] = [] // No unprotected headers for mock
        let toBeSigned = CBOR.array([
            CBOR.byteString(protected),
            CBOR.byteString(unprotected),
            CBOR.byteString([UInt8](payloadData)),
            CBOR.byteString([]) // Placeholder for signature
        ])
        let toBeSignedData = try CBOR.encode(toBeSigned)
        let signature = try privateKey.signature(for: toBeSignedData)

        let coseSign1 = CBOR.array([
            CBOR.byteString(protected),
            CBOR.byteString(unprotected),
            CBOR.byteString([UInt8](payloadData)),
            CBOR.byteString([UInt8](signature.derRepresentation))
        ])
        return Data(try CBOR.encode(coseSign1))
    }
}
