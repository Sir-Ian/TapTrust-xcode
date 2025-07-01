import XCTest
@testable import TapTrustSwift

final class CryptoTests: XCTestCase {
    func testVerifyFailsWithoutKey() {
        let payload: [String: Any] = ["doc": ["issuing_state": "ZZ"], "signature": Data()]
        XCTAssertFalse(CryptoUtils.verifySignature(parsed: payload))
    }
}
