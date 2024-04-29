#include <ThingSpeak.h> // Include the ThingSpeak library
#include <ESP8266WiFi.h>

// WiFi settings
const char* ssid = "Radhe_Radhe";
const char* password = "radheradhe@1411";

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


// #include <ESP8266WiFi.h>

// // WiFi settings
// const char* ssid = "";
// const char* password = "";

// #define GAS_SENSOR A0 // Analog pin connected to the MQ2 sensor
// #define GAS_SAMPLE_INTERVAL 2000 // Interval in milliseconds to sample the gas sensor



// WiFiClient client;

// void setup() {
//   Serial.begin(9600); // Start serial communication
//   connectWiFi(); // Connect to WiFi
//   ThingSpeak.begin(client); // Initialize ThingSpeak
// }

// void loop() {
//   int sensorValue = analogRead(GAS_SENSOR); // Read analog value from the sensor
//   float voltage = sensorValue * (5.0 / 1023.0); // Convert analog value to voltage
//   float lpgConcentration = getGasConcentration(voltage, -0.2, 0.5); // Calculate LPG concentration
//   float co2Concentration = getGasConcentration(voltage, -0.4, 1.0); // Calculate CO2 concentration
//   float alcoholConcentration = getGasConcentration(voltage, -0.3, 0.7); // Calculate alcohol concentration
//   float smokeConcentration = getGasConcentration(voltage, -0.5, 1.2); // Calculate smoke concentration

//   Serial.print("LPG Concentration: ");
//   Serial.print(lpgConcentration);
//   Serial.println(" ppm");

//   Serial.print("CO2 Concentration: ");
//   Serial.print(co2Concentration);
//   Serial.println(" ppm");

//   Serial.print("Alcohol Concentration: ");
//   Serial.print(alcoholConcentration);
//   Serial.println(" ppm");

//   Serial.print("Smoke Concentration: ");
//   Serial.print(smokeConcentration);
//   Serial.println(" ppm");



//   delay(GAS_SAMPLE_INTERVAL); // Wait for the next sample interval
// }

// float getGasConcentration(float voltage, float slope, float intercept) {
//   // Calculate gas concentration using the calibration curve
//   float concentration = slope * voltage + intercept;

//   return concentration;
// }

// void connectWiFi() {
//   Serial.println("Connecting to WiFi...");
//   WiFi.begin(ssid, password);
//   while (WiFi.status() != WL_CONNECTED) {
//     delay(1000);
//     Serial.println("Connecting...");
//   }
//   Serial.println("Connected to WiFi");
// }
