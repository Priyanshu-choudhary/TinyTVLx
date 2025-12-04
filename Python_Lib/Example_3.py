#Streaming Batches of Sensor Samples (IMU, GPS, etc.)

import struct
from tiny_tlv import TinyTLVTx, TinyTLVRx

# IMU sample (ax, ay, az in float32)
sample = struct.pack(">fff", 0.1, -0.2, 9.81)

tx = TinyTLVTx()
tx.begin(0x30)   # IMU_FRAME

tx.addTLV(0xA1, len(sample), sample)     # IMU accel
tx.addTLV(0xA2, 3, bytes([1,2,3]))       # Example status bytes

frame = tx.end()

# ---------------- RX ----------------
rx = TinyTLVRx()
for b in frame:
    if rx.feed(b):
        print("IMU Frame Received")
        rx.beginTLV()
        while True:
            tlv = rx.nextTLV()
            if tlv is None: break

            id_, L, data = tlv
            if id_ == 0xA1:
                ax, ay, az = struct.unpack(">fff", data)
                print("Accel:", ax, ay, az)
            else:
                print("Other TLV:", tlv)
