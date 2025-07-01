import XCTest

final class PackageTests: XCTestCase {
    func testSwiftPackageManifestExists() {
        let url = URL(fileURLWithPath: "Package.swift")
        XCTAssertTrue(FileManager.default.fileExists(atPath: url.path))
    }
}
