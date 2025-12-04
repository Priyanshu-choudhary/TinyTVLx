#Sending/Parsing a Dictionary as TLV

import json
from tiny_tlv import TinyTLVTx, TinyTLVRx

config = {
    "fps": 30,
    "mode": 2,
    "name": "camera_left"
}

# ---------------- TX ----------------
tx = TinyTLVTx()
tx.begin(0x20)    # FRAME TYPE = CONFIG

for key, val in config.items():
    encoded = str(val).encode()
    tx.addTLV(ord(key[0]), len(encoded), encoded)

frame = tx.end()
print("Sent:", frame)

# ---------------- RX ----------------
rx = TinyTLVRx()
for b in frame:
    if rx.feed(b):
        rx.beginTLV()
        out = {}

        while True:
            t = rx.nextTLV()
            if t is None: break
            id_, length, data = t
            out[chr(id_)] = data.decode()

        print("Decoded:", out)
