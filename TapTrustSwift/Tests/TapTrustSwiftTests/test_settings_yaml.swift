import XCTest

final class SettingsYamlTests: XCTestCase {
    func testSettingsYamlExists() {
        let url = URL(fileURLWithPath: "settings.yaml")
        XCTAssertTrue(FileManager.default.fileExists(atPath: url.path))
    }
}
