import XCTest
import SwiftCBOR
@testable import TapTrustSwift

final class CBORTests: XCTestCase {
    func testDecodePayloadReturnsExpectedKeys() throws {
        let payload: [String: Any] = ["foo": "bar", "num": 123]
        let bytes = try CBOR.encodeAny(payload)
        let data = Data(bytes)
        let result = try CBORCOSE.decodePayload(raw: data)
        XCTAssertEqual(result["foo"] as? String, "bar")
        XCTAssertEqual(result["num"] as? Int, 123)
    }
}
