// This code is currently intended as an example and may require adjustments.

#include <Stepper.h>

// Stepper motor configuration
const int stepsPerRevolution = 200;
const int motorSpeed = 60; // RPM

// Stepper motors: azimuth on pins 9-12, elevation on pins 5-8
Stepper azimuth(stepsPerRevolution, 9, 10, 11, 12);
Stepper elevation(stepsPerRevolution, 5, 6, 7, 8);

// Limit switch pins (avoid pins 0 and 1 which are RX/TX)
const int azLimitPin = 2;  // Azimuth home position
const int elLimitPin = 3;  // Elevation home position
const int calibrationButton = 4; // Manual calibration trigger

// State tracking
volatile boolean calibrationRequested = false;
int currentAz = 0;
int currentEl = 0;

void setup() {
    // Initialize limit switches and button
    pinMode(azLimitPin, INPUT_PULLUP);
    pinMode(elLimitPin, INPUT_PULLUP);
    pinMode(calibrationButton, INPUT_PULLUP);
    
    // Set motor speeds
    azimuth.setSpeed(motorSpeed);
    elevation.setSpeed(motorSpeed);
    
    // Initialize serial communication at 9600 baud
    Serial.begin(9600);
    Serial.println("SatTrack Controller initialized");
    Serial.println("Format: az,el (comma-separated integers for steps)");
    
    // Perform initial calibration
    calibrate();
}

void loop() {
    // Check for manual calibration button press
    if (digitalRead(calibrationButton) == LOW) {
        delay(50); // Debounce
        if (digitalRead(calibrationButton) == LOW) {
            Serial.println("Calibration triggered");
            calibrate();
            Serial.println("Calibration complete");
        }
        delay(500); // Prevent multiple triggers
    }
    
    // Check for incoming serial data
    if (Serial.available()) {
        String data = Serial.readStringUntil('\n');
        data.trim();
        
        if (data.length() > 0) {
            parseAndMove(data);
        }
    }
}

void parseAndMove(String data) {
    // Expected format: "az,el" where az and el are step counts
    // Example: "100,50"
    
    int commaIndex = data.indexOf(',');
    if (commaIndex == -1) {
        Serial.println("ERROR: Invalid format. Use: az,el");
        return;
    }
    
    // Extract azimuth and elevation values
    String azStr = data.substring(0, commaIndex);
    String elStr = data.substring(commaIndex + 1);
    
    // Convert to integers
    int azSteps = azStr.toInt();
    int elSteps = elStr.toInt();
    
    // Validate inputs
    if (azSteps == 0 && azStr != "0") {
        Serial.println("ERROR: Invalid azimuth value");
        return;
    }
    if (elSteps == 0 && elStr != "0") {
        Serial.println("ERROR: Invalid elevation value");
        return;
    }
    
    // Move motors
    Serial.print("Moving to Az:");
    Serial.print(azSteps);
    Serial.print(" El:");
    Serial.println(elSteps);
    
    // Move azimuth
    if (azSteps != 0) {
        azimuth.step(azSteps);
        currentAz += azSteps;
    }
    
    // Move elevation
    if (elSteps != 0) {
        elevation.step(elSteps);
        currentEl += elSteps;
    }
    
    Serial.println("OK");
}

void calibrate() {
    Serial.println("Starting calibration...");
    
    // Calibrate azimuth - move until limit switch is hit
    Serial.print("Calibrating azimuth...");
    while (digitalRead(azLimitPin) == HIGH) {
        azimuth.step(-1);
    }
    // Back off slightly from limit
    azimuth.step(5);
    currentAz = 0;
    Serial.println(" done");
    
    // Calibrate elevation - move until limit switch is hit
    Serial.print("Calibrating elevation...");
    while (digitalRead(elLimitPin) == HIGH) {
        elevation.step(-1);
    }
    // Back off slightly from limit
    elevation.step(5);
    currentEl = 0;
    Serial.println(" done");
}