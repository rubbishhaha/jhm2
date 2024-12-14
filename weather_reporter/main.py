import requests
import json
import pprint
parametervalue = {'dataType': 'warnsum', 'lang': 'en'}
response = requests.get("https://data.weather.gov.hk/weatherAPI/opendata/weather.php",params=parametervalue)
pprint.pp(json.dumps(response.json()))
#print(response)