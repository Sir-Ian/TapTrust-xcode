import XCTest
@testable import TapTrustSwift

final class ReadRawPayloadTests: XCTestCase {
    func testReadMobileIDReturnsData() throws {
        var reader = SystemReader()
        try? reader.open()
        let data = try? reader.readMobileID()
        reader.close()
        XCTAssertNotNil(data)
    }
}
