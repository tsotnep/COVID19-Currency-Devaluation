import json
import requests
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from collections import namedtuple
from datetime import date, timedelta
from matplotlib.ticker import MaxNLocator
import csv

#changables>>
currencies_list=["USD","GEL","RUB","PLN","RON","UAH","TRY","GBP","RON","CAD"]
start_date = date(2020, 1, 8)
end_date = date(2020, 3, 30)
api_key = '01bb2ac5412835d13b929aea8818591b' #you might need to update API key on this line
#<<changables

s_link='http://data.fixer.io/api/' #https://fixer.io/quickstart
s_dateKey='date='
s_date=''
s_access_key='?access_key='+api_key
s_currencies_key='&symbols='
s_currencies=','.join(currencies_list)
n_currencies=len(currencies_list)

d = [[] for reqjson in range(n_currencies)]

check_date = start_date
delta = timedelta(days=1)

while check_date <= end_date:
    check_date += delta
    s_date = check_date.strftime("%Y-%m-%d")
    apilink=s_link+s_date+s_access_key+s_currencies_key+s_currencies
    req = requests.get(apilink) 
    reqjson = json.loads(req.text, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    #print(reqjson)
    i=0 
    d[i].append(reqjson.rates.USD); i+=1
    d[i].append(reqjson.rates.GEL); i+=1
    d[i].append(reqjson.rates.RUB); i+=1
    d[i].append(reqjson.rates.PLN); i+=1
    d[i].append(reqjson.rates.RON); i+=1
    d[i].append(reqjson.rates.UAH); i+=1
    d[i].append(reqjson.rates.TRY); i+=1
    d[i].append(reqjson.rates.GBP); i+=1
    d[i].append(reqjson.rates.RON); i+=1
    d[i].append(reqjson.rates.CAD); i+=1



csvRawFileName="currencies/From_"+start_date.strftime("%Y-%m-%d")+" to_"+end_date.strftime("%Y-%m-%d")+"Raw.csv"
csvNorFileName="currencies/From_"+start_date.strftime("%Y-%m-%d")+" to_"+end_date.strftime("%Y-%m-%d")+"Normalized.csv"


with open(csvRawFileName, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(d)

#normalize
for i in range(len(currencies_list)):
    d[i][:] = [j / d[i][0] for j in d[i]] #current/day_before_first_corona_case
    #d[i][:] = [j / min(d[i]) for j in d[i]] #current/minimum

with open(csvNorFileName, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(d)


# draw
dates_d=np.arange(start_date,end_date+timedelta(days=1))
dates = np.datetime_as_string(dates_d)

fig, ax = plt.subplots()

for i in range(len(currencies_list)):
    ax.plot(dates, d[i], label=currencies_list[i])
    plt.xticks(rotation=30, fontsize=5)

ax.xaxis.set_major_locator(MaxNLocator(integer=True))
chartTitle='EUR price of DAILY_CURRENCY divided by BEFORE_CORONA_CURRENCY \n from '+start_date.strftime("%Y-%m-%d") + ' to '+end_date.strftime("%Y-%m-%d")
ax.set(xlabel='', ylabel='ratio: currency_day[i]/currency_8.1.2020', title=chartTitle)

ax.grid()
ax.legend()


fileName="currencies/From_"+start_date.strftime("%Y-%m-%d")+" to_"+end_date.strftime("%Y-%m-%d")+".png"
fig.savefig(fileName, dpi = 300)
#plt.show()
