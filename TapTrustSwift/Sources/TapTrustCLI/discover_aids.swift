import Foundation
import TapTrustSwift

// This is a stub for AID discovery. In a real implementation, you would enumerate known AIDs and attempt to select them on the NFC card.
// For now, just print the known AIDs from the Swift config.

print("Known AIDs:")
for (name, aid) in CoreNFCReader.knownAIDs {
    print("\(name): \(aid.map { String(format: "%02X", $0) }.joined())")
}
