import requests

latitude = 62.5
longitude = 10.44

url =  'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=%1.4f&lon=%1.4f' % (latitude, longitude)


headers = {
    'User-Agent': 'theCoop github.com/josmiseth/thecoop.git',
}

response = requests.get(url, headers=headers)

print(response.status_code)
#print(response.json())

met_data = response.json()

#for key in met_data:
#    print(key, ":", met_data[key])

instant_temperature = met_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["air_temperature"]

print(instant_temperature)
