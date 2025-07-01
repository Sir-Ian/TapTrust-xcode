# Building TapTrustSwift in Xcode

This repository contains a Swift package inside `TapTrustSwift/`. You can build and test it entirely from Xcode.

1. **Open the Package**
   - Launch Xcode and choose **File ▸ Open…**.
   - Select `TapTrustSwift/Package.swift` and wait while dependencies resolve.

2. **Choose a Scheme**
   - Use the scheme selector next to the run/stop buttons to pick either **TapTrustSwift** or **TapTrustCLI**.

3. **Build and Test**
   - Run **Product ▸ Build** to compile the selected target.
   - Run **Product ▸ Test** to execute `TapTrustSwiftTests`.

Xcode will use Swift Package Manager behind the scenes so no additional project file is needed.
