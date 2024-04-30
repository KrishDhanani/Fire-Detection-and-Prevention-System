#include <ThingSpeak.h> // Include the ThingSpeak library
#include <ESP8266WiFi.h>

// WiFi settings
const char* ssid = "Q234";
const char* password = "anmol0000";

#define flameDigitalPin D1 // Digital output pin for flame sensor
#define buzzerPin D2       // Digital output pin for buzzer

// ThingSpeak settings
unsigned long channelID =  2527010 ; // Your ThingSpeak channel ID
const char* writeAPIKey = "X9B5R6F0549IGNQO"; // Your ThingSpeak write API key
const long sensorID = 8989;

WiFiClient client;

void setup() {
    Serial.begin(9600); // Initialize serial communication for debugging
    connectWiFi(); // Connect to WiFi
    pinMode(flameDigitalPin, INPUT); // Set digital pin as input for flame sensor
    ThingSpeak.begin(client); // Initialize ThingSpeak
    pinMode(buzzerPin, OUTPUT);      // Set digital pin as output for buzzer
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
    
    // If flame is detected, activate the buzzer
    if (flameDigitalStatus == 0) {
        Serial.println("Flame detected!");
        digitalWrite(buzzerPin, HIGH); // Turn on the buzzer
        delay(1000);                    // Keep the buzzer on for 1 second
        digitalWrite(buzzerPin, LOW);  // Turn off the buzzer
    }

    // Update ThingSpeak channel with gas concentrations
    ThingSpeak.setField(1, flameDigitalStatus);
    ThingSpeak.setField(2, sensorID);
    ThingSpeak.writeFields(channelID, writeAPIKey);

    delay(1000); // Delay for stability
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
