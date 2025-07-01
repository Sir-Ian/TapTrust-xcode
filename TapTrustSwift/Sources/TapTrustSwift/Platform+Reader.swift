#if os(macOS)
import PCSC
typealias SystemReader = PCSCReader
#elseif canImport(CoreNFC)
import CoreNFC
typealias SystemReader = CoreNFCReader
#else
#error("Unsupported platform")
#endif
