#include <Stepper.h>

const int stepsPerRevolution = 200;

Stepper azimuth(stepsPerRevolution, 9, 10, 11, 12);
Stepper elevation(stepsPerRevolution, 5, 6, 7, 8);


void setup() {
    pinMode(1, INPUT_PULLUP);
    pinMode(2, INPUT_PULLUP);
    pinMode(3, INPUT_PULLUP);
    pinMode(4, INPUT_PULLUP);

    Serial.begin(9600);

}

void loop() {
    if(Serial.available() >= 4) {
        int azSteps = Serial.parseInt();
        int elSteps = Serial.parseInt();

        azimuth.step(azSteps);
        elevation.step(elSteps);
    }
    
}

void calibrate() {
    while(digitalRead(1) != HIGH) {
        azimuth.step(-1);
    }
    azimuth.step(10); // Back off a bit
}