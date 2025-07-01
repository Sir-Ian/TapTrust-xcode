// swift-tools-version: 6.1
import PackageDescription

let package = Package(
    name: "TapTrustSwift",
    platforms: [
        .iOS(.v15),
        .macOS(.v13)
    ],
    products: [
        .library(name: "TapTrustSwift", targets: ["TapTrustSwift"]),
        .executable(name: "TapTrustCLI", targets: ["TapTrustCLI"])
    ],
    dependencies: [
        .package(url: "https://github.com/SwiftDocOrg/SwiftCBOR.git", from: "0.6.0"),
        .package(
            url: "https://github.com/unistash-io/swift-pcsc.git",
            .upToNextMajor(from: "0.0.1")
        )
    ],
    targets: [
        .target(
            name: "TapTrustSwift",
            dependencies: [
                "SwiftCBOR",
                .product(name: "PCSC", package: "swift-pcsc", condition: .when(platforms: [.macOS]))
            ],
            path: "Sources/TapTrustSwift"
        ),
        .executableTarget(
            name: "TapTrustCLI",
            dependencies: ["TapTrustSwift"],
            path: "Sources/TapTrustCLI"
        ),
        .testTarget(
            name: "TapTrustSwiftTests",
            dependencies: ["TapTrustSwift"],
            path: "Tests/TapTrustSwiftTests"
        )
    ]
)
