import requests
import json
import sys
import datetime

sys.path.append('/home/josmi/projects/thecoop/')
import src as thecoop

latitude, longitude = thecoop.LATITUDE, thecoop.LONGITUDE
url = f'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={latitude}&lon={longitude}'
headers = {'User-Agent': 'theCoop github.com/josmiseth/thecoop.git'}
        
r = requests.get(url, headers=headers)


print(r.status_code)
#print(r.json)

met_data = r.json()
instant_temperature = met_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["air_temperature"]
#print(instant_temperature)

#print(met_data["properties"]["timeseries"])

# Get current date and set target timestamp at 13:00 UTC


# Get current date and set target timestamp at 13:00 UTC
today = datetime.date.today()

target_timestamp = f"{today}T13:00:00Z"
print(target_timestamp)
time_data = met_data["properties"]["timeseries"]
#print(target_timestamp)
# Extract the record matching the target timestamp
record = next((item for item in time_data if item['time'] == target_timestamp), None)

# Display the result
if record:
    #print("Record at 13:00 UTC on current date:")
    #print(record)
    day_temp = record["data"]["instant"]["details"]["air_temperature"]

    print(day_temp)
else:
    print("No record found for 13:00 UTC on the current date.")