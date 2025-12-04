#include <TinyTLVx.h>

TinyTLVTx tx;
TinyTLVRx rx;

void setup() {
    Serial.begin(115200);
}

void loop() {
    // ----------- TRANSMIT EXAMPLE --------------
    uint8_t frame[TTP_MAX_FRAME];

    uint16_t altitude = 1234;
    uint8_t battery   = 87;

    tx.begin(0x01); // TYPE = Telemetry
    tx.addTLV(0x03, 2, (uint8_t*)&altitude);
    tx.addTLV(0x05, 1, &battery);

    int bytes = tx.end(frame);
    Serial.println( bytes);

    delay(1000);


    // ----------- RECEIVE EXAMPLE --------------
    // while (Serial.available()) {
    //     uint8_t b = Serial.read();

    //     if (rx.feed(b)) {
    //         // Frame complete
    //         uint8_t type = rx.getType();
    //         Serial.print("\nGot frame type: ");
    //         Serial.println(type, HEX);

    //         rx.beginTLV();

    //         uint8_t id, len;
    //         uint8_t *data;

    //         while (rx.nextTLV(&id, &len, &data)) {
    //             Serial.print("ID: ");
    //             Serial.print(id);
    //             Serial.print("  LEN: ");
    //             Serial.print(len);
    //             Serial.print("  DATA: ");

    //             for (int i = 0; i < len; i++) {
    //                 Serial.print(data[i], HEX);
    //                 Serial.print(" ");
    //             }
    //             Serial.println();
    //         }
    //     }
    // }
}
