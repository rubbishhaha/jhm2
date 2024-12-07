import requests
import json
#response = requests.get("https://data.weather.gov.hk/weatherAPI/opendata/weather.php")
response = requests.get("http://api.open-notify.org/astros")
#print(json.dumps(response.json(), sort_keys=True, indent=4))
print(response)