import XCTest
@testable import TapTrustSwift

final class ReaderHelpersTests: XCTestCase {
    func testSelectEfComBuildsCorrectAPDU() {
        let apdu = APDU.buildAPDU(cla: 0x00, ins: 0xA4, p1: 0x02, p2: 0x0C, data: [0x12, 0x34])
        let expected: [UInt8] = [0x00, 0xA4, 0x02, 0x0C, 2, 0x12, 0x34]
        XCTAssertEqual(apdu, expected)
    }
    func testReadBinaryRangeMultipleBlocks() {
        // This is a stub. In a real test, you would mock the NFC reader and test chunked reads.
        // For now, just check the APDU chunking logic.
        let blockSize: UInt8 = 3
        let apdu1 = APDU.buildAPDU(cla: 0x00, ins: 0xB0, p1: 0x00, p2: 0x00, le: blockSize)
        let apdu2 = APDU.buildAPDU(cla: 0x00, ins: 0xB0, p1: 0x00, p2: 0x03, le: blockSize)
        XCTAssertEqual(apdu1, [0x00, 0xB0, 0x00, 0x00, 0x03])
        XCTAssertEqual(apdu2, [0x00, 0xB0, 0x00, 0x03, 0x03])
    }
}
