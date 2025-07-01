import XCTest
@testable import TapTrustSwift

final class DiscoverAIDsTests: XCTestCase {
    func testKnownAIDsNotEmpty() {
        XCTAssertFalse(CoreNFCReader.knownAIDs.isEmpty)
    }
}
