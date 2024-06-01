#include <ThingSpeak.h> // Include the ThingSpeak library
#include <ESP8266WiFi.h>

// WiFi settings
const char* ssid = "Vivo";
const char* password = "qwezxcasd";

#define flameDigitalPin D1 // Digital output pin for flame sensor
#define buzzerPin D2       // Digital output pin for buzzer

// ThingSpeak settings
unsigned long channelID = 2527010; // Your ThingSpeak channel ID
const char* writeAPIKey = "X9B5R6F0549IGNQO"; // Your ThingSpeak write API key
const long sensorID = 8989;

WiFiClient client;

// Flag to keep track of buzzer state
bool buzzerOnContinuously = false;

void setup() {
    Serial.begin(9600); // Initialize serial communication for debugging
    connectWiFi(); // Connect to WiFi
    pinMode(flameDigitalPin, INPUT); // Set digital pin as input for flame sensor
    ThingSpeak.begin(client); // Initialize ThingSpeak
    pinMode(buzzerPin, OUTPUT); // Set digital pin as output for buzzer
}

void connectWiFi() {
    Serial.println("Connecting to WiFi...");
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting...");
    }
    Serial.println("Connected to WiFi");
}

void loop() {
    // Read from flame sensor digital output pin
    int flameDigitalStatus = digitalRead(flameDigitalPin);

    // If flame is detected and the buzzer is not already on continuously
    if (flameDigitalStatus == 0) {
        Serial.println("Flame detected!");

        unsigned long startTime = millis(); // Record the start time
        while (millis() - startTime < 15000) { // 15 second delay
            digitalWrite(buzzerPin, HIGH); // Turn on the buzzer
            delay(500); // Buzzer stays on for 500ms
            digitalWrite(buzzerPin, LOW); // Turn off the buzzer
            delay(500); // Buzzer stays off for 500ms
        }

        // After 15 seconds, check the flame status again
        flameDigitalStatus = digitalRead(flameDigitalPin);

        if (flameDigitalStatus == 0) {
            // Keep the buzzer on continuously
            digitalWrite(buzzerPin, HIGH);
            buzzerOnContinuously = true;

            // Update ThingSpeak channel with flame status
            ThingSpeak.setField(1, flameDigitalStatus);
            ThingSpeak.setField(2, sensorID);
            ThingSpeak.writeFields(channelID, writeAPIKey);
        }
        else {
            // Keep the buzzer on continuously
            digitalWrite(buzzerPin, LOW);
            buzzerOnContinuously = false;

            // Update ThingSpeak channel with flame status
            ThingSpeak.setField(1, flameDigitalStatus);
            ThingSpeak.setField(2, sensorID);
            ThingSpeak.writeFields(channelID, writeAPIKey);
        }
    }

    // If no flame is detected, reset the buzzer state
    if (flameDigitalStatus != 0) {
        digitalWrite(buzzerPin, LOW);
        buzzerOnContinuously = false;
        ThingSpeak.setField(1, flameDigitalStatus);
        ThingSpeak.setField(2, sensorID);
        ThingSpeak.writeFields(channelID, writeAPIKey);
    }

    delay(1000); // Delay for stability
}
