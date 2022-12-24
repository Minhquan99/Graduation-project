#include <Wire.h>
void setup() {
Serial.begin(9600);     // opens serial port, baudrate : 9600 bps
}
 
void loop() {
 
        String str = Serial.readString();
        //String str = Serial.readString();
        Serial.print("Received: ");
        Serial.println(str);
    
}

