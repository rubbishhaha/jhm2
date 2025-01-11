import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

plt.figure(figsize=(10,6))
plt.xlabel("time(month)")
plt.ylabel("price(USD)")
syb = input("company:").upper()
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={syb}&interval=5min&apikey=82ESBKSY3WTLXIPO'
#url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={syb}&interval=5min&apikey=82ESBKSY3WTLXIPO'
r = requests.get(url)
datas = r.json()
stock = pd.DataFrame(data=datas["Time Series (Daily)"])
close_price = stock.iloc[3]
ix = list(close_price.index)
ix.reverse()
sx = [i for i in range(len(close_price.index))]
x = pd.to_datetime(ix)
y = [float(item) for item in close_price.values]
y.reverse()
plt.plot(x,y,label="actual price",color="green")
plt.title(f"Stock price for {syb}")
ax = np.array(sx).reshape((-1, 1))
ay = np.array(y)
model = LinearRegression().fit(ax, ay)
y_pred = model.predict(ax)
plt.plot(x,y_pred,linestyle='dashed',label="actual price",color="red")

plt.show()