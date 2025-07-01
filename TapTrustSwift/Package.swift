// swift-tools-version:6.1
import PackageDescription

let package = Package(
    name: "TapTrustSwift",
    platforms: [
        .iOS(.v15),
        .macOS(.v14)
    ],
    products: [
        .library(name: "TapTrustSwift", targets: ["TapTrustSwift"]),
        .executable(name: "TapTrustCLI", targets: ["TapTrustCLI"])
    ],
    dependencies: [
        .package(url: "https://github.com/valpackett/SwiftCBOR.git", from: "0.5.0"),     // Valpackett’s CBOR implementation :contentReference[oaicite:0]{index=0}
        .package(url: "https://github.com/apple/swift-crypto.git", from: "3.6.0"),       // Apple’s Swift-Crypto :contentReference[oaicite:1]{index=1}
        .package(
            url: "https://github.com/unistash-io/swift-pcsc.git",
            .upToNextMajor(from: "0.0.1")
        )
    ],
    targets: [
        .target(
            name: "TapTrustSwift",
            dependencies: [
                .product(name: "SwiftCBOR", package: "SwiftCBOR"),
                .product(name: "Crypto",    package: "swift-crypto"),
                .product(name: "PCSC",      package: "swift-pcsc", condition: .when(platforms: [.macOS]))
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
