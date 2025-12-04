# **TinyTLV Protocol**

A minimal, deterministic TLV-based framing protocol for microcontrollers, embedded links, WebSockets, UART, or any stream transport.

This protocol is designed to be:

* **Zero-dependency**
* **Binary-safe**
* **Stream-parseable**
* **Interoperable** between **Arduino/C++** and **Python**

---

# **1. Why TinyTLV?**

Most embedded data links need:

* Clear frame boundaries
* Strong data typing
* Recovery from corrupted bytes
* Ability to carry mixed data (ints, floats, strings, raw structs)

TinyTLV solves all of this with a simple TLV format + XOR checksum.

---

# **2. Frame Structure**

Every frame follows the same layout:

```
+--------+--------+--------+--------+--------+-----+----------+
|  STX   |  LEN   |  TYPE  |  TLVs..................| CHECKSUM |
+--------+--------+--------+--------+--------+-----+----------+
   1B       1B       1B            variable       1B
```

### **Fields**

| Field        | Description                                            |
| ------------ | ------------------------------------------------------ |
| **STX**      | Start-of-frame marker (`0x02`)                         |
| **LEN**      | Number of bytes after LEN until checksum (TYPE + TLVs) |
| **TYPE**     | Application-defined frame type (1B)                    |
| **TLVs**     | Sequence of TLVs                                       |
| **CHECKSUM** | XOR of all bytes in `[TYPE + TLVs]`                    |

---

# **3. TLV Element Format**

Each TLV inside the frame:

```
+--------+---------+----------------------+
|   ID   |  LEN    |  DATA (LEN bytes)    |
+--------+---------+----------------------+
    1B      1B      variable
```

* `ID` = TLV tag
* `LEN` = length of `DATA`
* `DATA` = binary payload

---

# **4. Example Frame (Annotated)**

```
02   0A   10   01 02  00 64   02 01  FF   8B
│    │    │    │    │ └──100 │  │ └── 255 │
│    │    │    │    │        │  │         └ checksum
│    │    │    │    │        │  └ TLV #2 len=1
│    │    │    │    │        └ TLV #1 data=0x0064
│    │    │    │    └ TLV #1 len=2
│    │    │    └ TLV #1 id=1
│    │    └ TYPE=0x10
│    └ LEN=10 bytes
└ STX
```

---

# **5. Encoding Rules**

### **5.1 Checksum**

```
CHECKSUM = XOR of every byte from TYPE to last TLV byte
```

### **5.2 Maximum Size**

```
MAX FRAME = 256 bytes
```

---

# **6. Arduino / C++ Usage**

Below is the minimal Arduino usage with the TinyTLVx library.

---

## **6.1 Encoding (TX)**

```cpp
#include "TinyTLVx.h"

TinyTLVTx tx;

void sendTelemetry() {
    tx.begin(0x10);               // frame type

    uint16_t temp = 123;
    tx.addTLV(0x01, 2, (uint8_t*)&temp);

    uint8_t health = 5;
    tx.addTLV(0x02, 1, &health);

    uint16_t len;
    uint8_t* frame = tx.end(len); // returns pointer + length

    Serial.write(frame, len);
}
```

---

## **6.2 Decoding (RX)**

```cpp
#include "TinyTLVx.h"

TinyTLVRx rx;

void loop() {
    while (Serial.available()) {
        uint8_t b = Serial.read();
        if (rx.feed(b)) {
            uint8_t type = rx.getType();
            rx.beginTLV();

            while (rx.hasNext()) {
                TLV t = rx.next();
                Serial.print("ID=");
                Serial.print(t.id);
                Serial.print(" LEN=");
                Serial.println(t.len);
            }
        }
    }
}
```

---

# **7. Python Usage**

This uses the exact classes from your implementation (`TinyTLVTx`, `TinyTLVRx`).

---

## **7.1 Encoding**

```python
from tiny_tlv import TinyTLVTx

tx = TinyTLVTx()
tx.begin(0x10)

tx.addTLV(0x01, 2, (123).to_bytes(2, 'big'))
tx.addTLV(0x02, 1, bytes([5]))

frame = tx.end()
print("Frame:", frame)
```

---

## **7.2 Decoding**

```python
from tiny_tlv import TinyTLVRx

rx = TinyTLVRx()

for b in frame:
    if rx.feed(b):
        print("Type:", hex(rx.getType()))
        rx.beginTLV()

        while True:
            tlv = rx.nextTLV()
            if tlv is None:
                break
            print(tlv)
```

---

# **8. Full Example – Cross-Platform Interop**

Arduino sends:

```cpp
tx.begin(0x30);
float ax = 0.1, ay = -0.2, az = 9.81;
tx.addTLV(0xA1, sizeof(float)*3, (uint8_t*)&ax);
sendFrame(tx);
```

Python receives:

```python
id_, length, data = tlv
ax, ay, az = struct.unpack(">fff", data)
```

Works both ways.
Binary-safe.
Identical layout.

---

# **9. Recommended Frame Types**

| Type | Meaning            |
| ---- | ------------------ |
| 0x01 | RC control         |
| 0x10 | Telemetry          |
| 0x20 | Configuration      |
| 0x30 | IMU / sensor burst |
| 0x40 | Chat / messages    |
| 0x50 | Debug / logs       |

---

# **10. Best Practices**

* Keep TLV IDs small (`1–50`)
* Use little-endian on MCU, big-endian on Python → or explicitly choose one
* Always check length before unpacking
* Reset parser after each valid/invalid frame
* Do not rely on timing, rely on STX + LEN

---

# **11. License**

MIT.
Use it for anything.

---

