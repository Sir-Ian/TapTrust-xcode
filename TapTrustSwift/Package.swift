// swift-tools-version: 6.1
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
    name: "TapTrustSwift",
    platforms: [.iOS(.v15)],
    dependencies: [
        .package(url: "https://github.com/SwiftDocOrg/SwiftCBOR.git", from: "0.6.0")
    ],
    targets: [
        .executableTarget(
            name: "TapTrustSwift",
            dependencies: ["SwiftCBOR"]
        ),
        .testTarget(
            name: "TapTrustSwiftTests",
            dependencies: ["TapTrustSwift"]
        )
    ]
)
