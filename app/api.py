from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData
import matplotlib.pyplot as plt
API_Key = "W1IZOWOCKK0XHEFE"
ts2 = TimeSeries(key=API_Key, output_format='pandas')
data = ts2.get_monthly_adjusted(symbol='AMZN')
#f = open = ("apiData.txt", "w")
#for t in data:
#    t0 = t[0]
#    t1 = t[1]
#    f.write(t0 + " " + t1 + "\n")
#print(f.read())
#f.close()
#print("index:", data.index)
#print(data[0]['4. close'])
data[0]['5. adjusted close'].plot()
plt.title('Closing Price of AMZN')
plt.show()
