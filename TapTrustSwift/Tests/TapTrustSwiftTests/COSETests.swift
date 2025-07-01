import XCTest
@testable import TapTrustSwift
import SwiftCBOR

final class COSETests: XCTestCase {
    func testDecodePlainCBOR() throws {
        let obj: [String: Any] = ["foo": "bar"]
        let bytes = try CBOR.encodeAny(obj)
        let data = Data(bytes)
        let result = try CBORCOSE.decodePayload(raw: data)
        XCTAssertEqual(result["foo"] as? String, "bar")
    }
}
