from datetime import datetime
import requests
import time
import pytz

LAST_PROCESSED_ENTRY_FILE = "last_processed_entry.txt"

def read_last_processed_entry():
    try:
        with open(LAST_PROCESSED_ENTRY_FILE, "r") as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return 0

def write_last_processed_entry(last_processed_entry_id):
    with open(LAST_PROCESSED_ENTRY_FILE, "w") as file:
        file.write(str(last_processed_entry_id))

def get_data(api_key):
    last_processed_entry_id = read_last_processed_entry()
    parameter = {'api_key': api_key}
    try:
        response = requests.get(url='https://api.thingspeak.com/channels/2527010/feeds.json', params=parameter)
        response.raise_for_status()
        data = response.json()['feeds']
        return data[last_processed_entry_id:], len(data)
    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
        return None, None

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


def main():
    THINGSPEAK_API_KEY = "60X95M3U43W68XUI"
    while True:
        data, total_entries = get_data(THINGSPEAK_API_KEY)
        if data and total_entries is not None:
            for entry in data:
                if int(entry['field1']) == 1:
                    print("detecting 1")
                    print(datetime.now().strftime('%H:%M:%S'))
                if int(entry['field1']) == 0:
                    flame_detected_time = convert_to_ist(entry['created_at'])
                    if flame_detected_time:
                        print("Flame Sensor ID:", entry['field2'])
                        print("Flame Detected Time (IST):", flame_detected_time)
                        time.sleep(15)
            last_processed_entry_id = read_last_processed_entry() + 1
            write_last_processed_entry(last_processed_entry_id)
        time.sleep(1)

if __name__ == "__main__":
    main()
