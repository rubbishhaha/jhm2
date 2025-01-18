import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from datetime import timedelta

syb = input("company: ").upper()
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={syb}&interval=5min&apikey=82ESBKSY3WTLXIPO&outputsize=full'
#url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={syb}&interval=5min&apikey=82ESBKSY3WTLXIPO'
r = requests.get(url)
datas = r.json()
stock = pd.DataFrame(data=datas["Time Series (Daily)"])
close_price = stock.iloc[3]
date_u = pd.to_datetime(input("starting date (YYYY-MM-DD): "))
date_v = pd.to_datetime(input("ending date   (YYYY-MM-DD): "))

def data_calculate(close_price,predict_day,du,dv):
    r_price = list(close_price.index)
    r_price.reverse()
    d_price = pd.to_datetime(r_price)
    x = list(filter((3).__ne__, [date if (date - du).days >= 0 and (dv - date).days >= 0 else 3 for date in d_price]))
    ux = list(filter((3).__ne__, [date if(date - dv).days >= -2 else 3 for date in d_price]))

    y = [float(i) for i in list(close_price.loc[[str(i)[:10] for i in x]])]
    uy = [float(i) for i in list(close_price.loc[[str(i)[:10] for i in ux]])]
    

    x_index = [date - x[0] for date in x]
    x_index = [r.days for r in x_index]
    x_index_pre = x_index + [u + x_index[-1] for u in range(predict_day)]
    
    model = LinearRegression().fit(np.array(x_index).reshape((-1, 1)), np.array(y))
    poly = PolynomialFeatures (degree=2, include_bias=False)
    poly_features = poly.fit_transform(np.array(x_index).reshape((-1, 1)))
    poly_reg_model = LinearRegression()
    poly_reg_model.fit(poly_features, y)

    pre_y2 = poly_reg_model.predict(poly.fit_transform(np.array(x_index_pre).reshape((-1, 1))))
    pre_y1 = model.predict(np.array(x_index_pre).reshape((-1, 1)))
    pre_x = [x[0] + timedelta(w) for w in x_index_pre]

    return x,y,pre_x,pre_y1,pre_y2,ux,uy
'''''
ix = list(close_price.index)
ix.reverse()
sx = [i for i in range(len(close_price.index)+15)]
elborated_day = pd.to_datetime([pd.to_datetime(ix[-1]) + timedelta(3*w+3) for w in range(15)])
x = np.concatenate((pd.to_datetime(ix), elborated_day), axis=None)
y = [float(item) for item in close_price.values]
y.reverse()
price, = plt.plot(x[:len(y)],y,label="actual price",color="green")
ax = np.array(sx[:len(y)]).reshape((-1, 1))
ay = np.array(y)
x,y,pre_x,pre_y = data_calculate(close_price)
y_pred = model.predict(np.array(sx).reshape((-1, 1)))
predict, = plt.plot(x,y_pred,linestyle='dashed',label="line regression",color="red")
'''''''''

#x,y,pre_x,pre_y = data_calculate(close_price,1000)
#price, = plt.plot(x,y,label="actual price",color="green")
#predict, = plt.plot(pre_x,pre_y,linestyle='dashed',label="linear regression",color="red")

plt.figure(figsize=(10,6))
plt.xlabel("time(month)")
plt.ylabel("price(USD)")
plt.grid()

x,y,pre_x,pre_y1,pre_y2,ux,uy = data_calculate(close_price,int(round((date_v-date_u).days*0.2)),date_u,date_v)
#print (f"\n\n{x}\n{ux}\n\n{y}\n{uy}")

#tprice, = plt.plot(pd.to_datetime(close_price.index),[float(x) for x in close_price.values],color="yellow")
pprice, = plt.plot(x,y,label="data price",color="green")
fprice, = plt.plot(ux,uy,label="experimental price",color="purple")
predict1, = plt.plot(pre_x,pre_y1,linestyle='dashed',color="red")
predict2, = plt.plot(pre_x,pre_y2,linestyle='dashed',color="blue")

plt.title(f"Stock price for {syb}")
plt.legend(["data price","experimental price","Linear regression","Polynomial regression"], fontsize="x-large")

plt.savefig("figure.png", dpi='figure', format=None)