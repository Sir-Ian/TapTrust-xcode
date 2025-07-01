import Foundation
import TapTrustSwift

// Usage: swift run generate_mock_payload
let data = try MockPayloadGenerator.generateMockCOSEPayload()
let url = URL(fileURLWithPath: "examples/mock_cose_payload.cbor")
try FileManager.default.createDirectory(at: url.deletingLastPathComponent(), withIntermediateDirectories: true)
try data.write(to: url)
print("✅ Wrote COSE payload to \(url.path)")
