import Foundation

public struct APDU {
    public static func buildAPDU(cla: UInt8, ins: UInt8, p1: UInt8, p2: UInt8, data: [UInt8] = [], le: UInt8? = nil) -> [UInt8] {
        var apdu: [UInt8] = [cla, ins, p1, p2]
        if !data.isEmpty {
            apdu.append(UInt8(data.count))
            apdu.append(contentsOf: data)
        }
        if let le = le {
            apdu.append(le)
        }
        return apdu
    }
    public static func buildSelectApplet(aid: [UInt8]) -> [UInt8] {
        guard !aid.isEmpty, aid.count <= 255 else { return [] }
        return buildAPDU(cla: 0x00, ins: 0xA4, p1: 0x04, p2: 0x00, data: aid)
    }
    public static func parseResponse(_ resp: [UInt8]) -> (data: [UInt8], sw1: UInt8, sw2: UInt8)? {
        guard resp.count >= 2 else { return nil }
        let data = Array(resp.dropLast(2))
        let sw1 = resp[resp.count - 2]
        let sw2 = resp[resp.count - 1]
        return (data, sw1, sw2)
    }
    public static func isSuccess(sw1: UInt8, sw2: UInt8) -> Bool {
        return sw1 == 0x90 && sw2 == 0x00
    }
}
