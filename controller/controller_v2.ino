#include <AccelStepper.h>

// This code assumes TMC2209 drivers in Step/Dir mode.

#define MOTOR_INTERFACE_TYPE 1

// Motor parameters
const int stepsPerRevolution = 3200; // At 1/16 microstepping
const int maxSpeed = 5000; // Steps per second
const int acceleration = 500; // Steps per second²

// Azimuth motor driver pins
const int dirPinAz = 2;
const int stepPinAz = 3;
const int enablePinAz = 4;
const int microstepPin1Az = 5;
const int microstepPin2Az = 6;

// Elevation motor driver pins
const int dirPinEl = 8;
const int stepPinEl = 9;
const int enablePinEl = 10;
const int microstepPin1El = 11;
const int microstepPin2El = 12;

// AccelStepper instances
AccelStepper azimuth(MOTOR_INTERFACE_TYPE, stepPinAz, dirPinAz);
AccelStepper elevation(MOTOR_INTERFACE_TYPE, stepPinEl, dirPinEl);

// Limit switch pins
const int limitSwitchPin1 = 7;
const int limitSwitchPin2 = 13;

void setup() {
    // Configure pins
    pinMode(enablePinAz, OUTPUT);
    pinMode(enablePinEl, OUTPUT);
    pinMode(microstep1PinAz, OUTPUT);
    pinMode(microstep2PinAz, OUTPUT);
    pinMode(microstep1PinEl, OUTPUT);
    pinMode(microstep2PinEl, OUTPUT);

    // Enable motors
    digitalWrite(enablePinAz, LOW);
    digitalWrite(enablePinEl, LOW);

    // Configure microstepping (1/32 steps)
    digitalWrite(microstepPin1Az, LOW);
    digitalWrite(microstepPin2Az, HIGH);

    digitalWrite(microstepPin1El, LOW);
    digitalWrite(microstepPin2El, HIGH);

    // Motor configuration
    azimuth.setMaxSpeed(maxSpeed);
    azimuth.setAcceleration(acceleration);

    elevation.setMaxSpeed(maxSpeed);
    elevation.setAcceleration(acceleration);

    Serial.begin(9600);
    Serial.println("Initialized, beginning calibration...");
    

}

void loop() {

}

void calibrate() {
    // Move azimuth to limit switch
    while(digitalRead(limitSwitchPin1) == LOW) {
        azimuth.setSpeed(-maxSpeed / 2);
        azimuth.runSpeed();
    }
}