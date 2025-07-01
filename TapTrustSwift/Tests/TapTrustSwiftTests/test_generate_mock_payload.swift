import XCTest
@testable import TapTrustSwift

final class GenerateMockPayloadTests: XCTestCase {
    func testGenerateMockCOSEPayload() throws {
        let data = try MockPayloadGenerator.generateMockCOSEPayload()
        XCTAssertFalse(data.isEmpty)
    }
}
