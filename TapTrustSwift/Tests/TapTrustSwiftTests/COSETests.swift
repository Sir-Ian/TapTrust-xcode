import XCTest
@testable import TapTrustSwift

final class COSETests: XCTestCase {
    func testDecodePlainCBOR() throws {
        let obj: [String: Any] = ["foo": "bar"]
        let data = try CBOR.encode(obj)
        let result = try CBORCOSE.decodePayload(raw: data)
        XCTAssertEqual(result["foo"] as? String, "bar")
    }
}
