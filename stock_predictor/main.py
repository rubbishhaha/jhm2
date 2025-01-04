import requests
import json
url = 'https://www.alphavantage.co/query?function=HISTORICAL_OPTIONS&symbol=IBM&apikey=T8IS9FYQY61PODGT'
r = requests.get(url)
data = r.json()

print(data)