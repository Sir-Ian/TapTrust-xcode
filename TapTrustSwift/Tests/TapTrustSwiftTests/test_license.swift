import XCTest

final class LicenseTests: XCTestCase {
    func testLicenseFileExists() {
        let url = URL(fileURLWithPath: "LICENSE")
        XCTAssertTrue(FileManager.default.fileExists(atPath: url.path))
    }
}
