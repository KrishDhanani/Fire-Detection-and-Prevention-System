// #define BLYNK_PRINT Serial
#include <ESP8266WiFi.h>
// #include <BlynkSimpleEsp8266.h>
// BlynkTimer timer;
// char auth[] = "Q2jEWbbXh2vf7rfOafW3LoATOPAsNImQ"; //Enter the Auth Code sent to the registered email address from the Blynk App
 
// char ssid[] = "wifi-username"; //Enter the Wifi Username
// char pass[] = "password";	   //Enter the Wifi Password
int flag=0;
const int buttonPin = D1; // Define the pin connected to the fire detection sensor
const int buzzerPin = D4; // Define the pin connected to the buzzer
void notifyOnFire()
{
  int isButtonPressed = digitalRead(buttonPin);
  if (isButtonPressed==0 && flag==0) {
    Serial.println("Fire in the House");
    // Blynk.notify("Alert : Fire in the House");
    flag=1;
  }
  else if (isButtonPressed==1)
  {
    flag=0;
  }
}
void ledblink(){
  int isButtonPressed = digitalRead(buttonPin);
  if (isButtonPressed==0 && flag==0) {
    Serial.println("Fire in the House");
    digitalWrite(buzzerPin, HIGH);
    flag=1;
  }
  else if (isButtonPressed==1)
  {
    digitalWrite(buzzerPin, LOW);
    flag=0;
  }
}
void setup()
{
  Serial.begin(9600);
  // Blynk.begin(auth, ssid, pass);
  pinMode(buttonPin,INPUT);
  // timer.setInterval(1000L,notifyOnFire); 
  // timer.setInterval(1000L,ledblink); 
  pinMode(buzzerPin, OUTPUT);
}
void led(){
  digitalWrite(buzzerPin, HIGH);
  delay(1000);
  digitalWrite(buzzerPin, LOW);
  delay(1000);
}
void loop()
{
  // Blynk.run();
  // timer.run();
  // ledblink();
  led();
}