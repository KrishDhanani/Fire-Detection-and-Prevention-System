from datetime import datetime, timedelta
import pytz
import requests
import time

# def get_current_zulu_time_with_delay(delay_seconds=15):
#     utc_time = datetime.utcnow() # Get the current time in UTC
#     utc_timezone = pytz.timezone('UTC') # Set the timezone to UTC
#     localized_time = utc_timezone.localize(utc_time)        # Localize the UTC time to UTC timezone
#     delayed_time = localized_time + timedelta(seconds=delay_seconds)    # Add the delay
#     return delayed_time.strftime('%Y-%m-%dT%H:%M:%SZ')

# Example usage
# current_zulu_time_with_delay = get_current_zulu_time_with_delay()
# print("Current Zulu time with 15-second delay:", current_zulu_time_with_delay)


THINGSPEAK_API_KEY = "60X95M3U43W68XUI"
parameter = {
    'api_key': THINGSPEAK_API_KEY,
}

def convert_to_ist(zulu_time_str):
    try:
        zulu_time = datetime.strptime(zulu_time_str, '%Y-%m-%dT%H:%M:%SZ')
        zulu_timezone = pytz.timezone('UTC')
        indian_timezone = pytz.timezone('Asia/Kolkata')
        indian_time = zulu_timezone.localize(zulu_time).astimezone(indian_timezone)
        return indian_time.strftime('%H:%M:%S')
    except ValueError as e:
        print("Error converting time:", e)
        return None

while True:
    response = requests.get(url='https://api.thingspeak.com/channels/2527010/feeds.json', params=parameter)
    response.raise_for_status()
    data = response.json()['feeds']
    zulu_time = data[len(data) - 1]['created_at'][11:].replace('T', ' ').replace('Z', '')

    print(data)
    if int(data[len(data) - 1]['field1']) == 1:
        print("Flame Not detected \nIndian time:", datetime.now().time())
    if int(data[len(data)-1]['field1']) == 0:
        flame_detected_time = convert_to_ist(zulu_time)
        if flame_detected_time:
            print("Flame Sensor ID:", data['field2'], "\nFlame Detected Time (IST):", flame_detected_time)
    time.sleep(15)

