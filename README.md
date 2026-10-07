# 🔥 Fire Detection and Prevention System

An IoT system that monitors a room 24/7, detects fire using sensors, and automatically alerts the user and, if needed, the nearest fire department with the exact location.

## Overview
This project combines **hardware and software**. The device sits in the center of a room and continuously reads flame and smoke sensors. When a fire is detected, the data is sent to the **ThingSpeak API**, and the system reacts in stages:

1. The device triggers a **light and buzzer** on site.
2. The user is notified through **SMS (Twilio)** and **email (SMTP)**.
3. The user has **10 seconds** to press the button on the device to cancel a false alarm.
4. If nobody responds, an alert goes to the **nearest fire department**, including the user's details (floor and contact information) and the device's **latitude and longitude** so responders can find the place faster.

## Features
- 24/7 environment monitoring with flame and smoke sensors
- On-site alarm with light and buzzer
- Digital alerts via Twilio (SMS) and SMTP (email)
- 10-second button confirmation to prevent false alarms
- Automatic escalation to the nearest fire department
- Location sharing with latitude and longitude on an OpenStreetMap map
- Web dashboard built with Flask
- Data stored in SQLite3

## Tech stack

**Hardware:** ESP8266 · Flame sensor · Smoke sensor · Buzzer · LED · Push button

**Software:** Python · Flask · HTML · CSS · Bootstrap · Leaflet.js · SQLite3

**Services and APIs:** ThingSpeak · Twilio · SMTP · OpenStreetMap

## How it works
```
Sensors (flame, smoke) → ESP8266 → ThingSpeak API → Flask backend
                                                        │
                       ┌────────────────────────────────┤
                       ▼                                ▼
          Light + buzzer, SMS (Twilio),       No button press in 10 s?
          email (SMTP) to user                        │
                                                      ▼
                                       Alert to nearest fire department
                                       (user details + latitude/longitude)
```

## Screenshots
<!-- Add photos of the device and the dashboard here -->
![Device](images/device.jpg)
![Dashboard](images/dashboard.png)

## How to run

**1. Hardware**
- Connect the sensors, buzzer, LED and button to the ESP8266 (add a wiring diagram or pin table here).
- Upload the firmware with the Arduino IDE.

**2. Software**
```bash
git clone https://github.com/KrishDhanani/Fire-Detection-and-Prevention-System.git
cd Fire-Detection-and-Prevention-System
pip install -r requirements.txt
python app.py
```

**3. Configuration**
Add your own keys (never commit them to GitHub):
- ThingSpeak channel ID and API key
- Twilio account SID, auth token and phone number
- SMTP email and app password

## What I learned / next steps
- Combining hardware (ESP8266) and a web backend in one system
- Working with real-time APIs and messaging services
- Next: add more sensors, a mobile-friendly dashboard, and automatic detection of the nearest fire station
