import XCTest
@testable import TapTrustSwift

final class APDUTests: XCTestCase {
    func testBuildSelectApplet() {
        // Placeholder: simply ensure the known AID is correct length
        XCTAssertEqual(CoreNFCReader.knownAIDs["ISO18013"]?.count, 8)
    }
}
