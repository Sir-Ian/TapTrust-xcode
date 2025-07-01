import Foundation
import TapTrustSwift

var reader = SystemReader()
do {
    try reader.open()
    let data = try reader.readMobileID()
    reader.close()
    print("Read \(data.count) bytes:\n\(data.map { String(format: "%02X", $0) }.joined())")
} catch {
    print("Error: \(error)")
}
