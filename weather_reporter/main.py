import requests
import json
#response = requests.get("https://data.weather.gov.hk/weatherAPI/opendata/weather.php")
#response = requests.get("http://api.open-notify.org/astros")
response = requests.get("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/London%2CUK/last7days?unitGroup=metric?&key=YOUR_API_KEY")
print(json.dumps(response.json(), sort_keys=True, indent=4))
#print(response)