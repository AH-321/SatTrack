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

// Global variables
volatile bool calibrated = false;
int currentAz = 0;
int currentEl = 0;

void setup() {
    // Configure pins
    pinMode(enablePinAz, OUTPUT);
    pinMode(enablePinEl, OUTPUT);
    pinMode(microstepPin1Az, OUTPUT);
    pinMode(microstepPin2Az, OUTPUT);
    pinMode(microstepPin1El, OUTPUT);
    pinMode(microstepPin2El, OUTPUT);
    pinMode(limitSwitchPin1, INPUT_PULLUP);
    pinMode(limitSwitchPin2, INPUT_PULLUP);

    // Enable motors
    digitalWrite(enablePinAz, LOW);
    digitalWrite(enablePinEl, LOW);

    // Configure microstepping (1/16 steps)
    digitalWrite(microstepPin1Az, HIGH);
    digitalWrite(microstepPin2Az, HIGH);

    digitalWrite(microstepPin1El, HIGH);
    digitalWrite(microstepPin2El, HIGH);

    // Motor configuration
    azimuth.setMaxSpeed(maxSpeed);
    azimuth.setAcceleration(acceleration);

    elevation.setMaxSpeed(maxSpeed);
    elevation.setAcceleration(acceleration);

    Serial.begin(9600);
    Serial.println("Initialized, beginning calibration...");
    calibrate();

}

void loop() {
    if (!calibated) {
        Serial.println("Calibration error.)");
        break;
    }

}

void calibrate() {
    // Move azimuth to limit switch
    Serial.println("Moving...");
    while(digitalRead(limitSwitchPin1) == HIGH) {
        azimuth.setSpeed(-maxSpeed / 2);
        azimuth.runSpeed();
    }
    Serial.println("Switch triggered, setting position to 0");
    azimuth.setCurrentPosition(0);
    azimuth.moveTo(stepsPerRevolution / 4); // Move to 90 degrees

    while(azimuth.distanceToGo() != 0) {
        azimuth.run();
    }
    Serial.println("Azimuth calibrated, beginning elevation calibration...");
    
    Serial.println("Moving...");
    while(digitalRead(limitSwitchPin2) == HIGH) {
        elevation.setSpeed(-maxSpeed / 2);
        elevation.runSpeed();
    }
    Serial.println("Switch triggered, setting position to 0");
    elevation.setCurrentPosition(0);
    elevation.moveTo(stepsPerRevolution / 4); // Move to 90 degrees

    while(elevation.distanceToGo() != 0) {
        elevation.run();
    }
    
    Serial.println("Elevation calibrated, calibration complete.");
    calibrated = true;

}