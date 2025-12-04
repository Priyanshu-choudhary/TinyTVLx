# Example 1 — Encode/Decode Simple Sensor Telemetry (int, float, string)


from tiny_tlv import TinyTLVTx, TinyTLVRx

# ------------------- TX SIDE -------------------
tx = TinyTLVTx()
tx.begin(0x10)  # Frame type = TELEMETRY

tx.addTLV(0x01, 2, (123).to_bytes(2, 'big'))        # temperature int16
tx.addTLV(0x02, 4, bytearray(struct.pack(">f", 3.14)))  # float
tx.addTLV(0x03, len(b"OK"), b"OK")                  # string

frame = tx.end()
print("TX Frame:", frame)

# ------------------- RX SIDE -------------------
rx = TinyTLVRx()

for b in frame:
    if rx.feed(b):
        print("Frame type:", hex(rx.getType()))
        rx.beginTLV()

        while True:
            tlv = rx.nextTLV()
            if tlv is None: 
                break
            print(tlv)   # (id, length, data)
