import XCTest
@testable import TapTrustSwift

final class ExamplesTests: XCTestCase {
    func testExamplesDirectoryExists() {
        let url = URL(fileURLWithPath: "examples")
        var isDir: ObjCBool = false
        let exists = FileManager.default.fileExists(atPath: url.path, isDirectory: &isDir)
        XCTAssertTrue(exists && isDir.boolValue)
    }
}
