import XCTest

final class TrustAnchorsTests: XCTestCase {
    func testTrustAnchorsDirectoryExists() {
        let url = URL(fileURLWithPath: "trust_anchors")
        var isDir: ObjCBool = false
        let exists = FileManager.default.fileExists(atPath: url.path, isDirectory: &isDir)
        XCTAssertTrue(exists && isDir.boolValue)
    }
}
