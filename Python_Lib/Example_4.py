#Multi-Channel Chat/Message Protocol

from tiny_tlv import TinyTLVTx, TinyTLVRx

# Frame with 3 message types
tx = TinyTLVTx()
tx.begin(0x40)  # CHAT/META FRAME

tx.addTLV(0x01, len(b"HELLO"), b"HELLO")          # text msg
tx.addTLV(0x02, 1, bytes([5]))                    # priority
tx.addTLV(0x03, len(b"\x01\x02\x03"), b"\x01\x02\x03") # raw binary payload

frame = tx.end()

rx = TinyTLVRx()
for b in frame:
    if rx.feed(b):
        print("Chat frame received")
        rx.beginTLV()
        while True:
            item = rx.nextTLV()
            if item is None: break
            print(item)
    