import json
import requests
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from collections import namedtuple
from datetime import date, timedelta
from matplotlib.ticker import MaxNLocator
import csv
from itertools import cycle

#changables>>
currencies_list=["USD","GEL","RUB","PLN","RON","UAH","TRY","GBP","RON","CAD","AED","AMD","AZN","IRR","MXN"] #just add any if available : https://fixer.io/symbols
start_date = date(2020, 1, 8)
end_date = date(2020, 3, 30)
reference_date = date(2020, 1, 8) #all list of currencies will be divided by that day's currency
api_key = '01bb2ac5412835d13b929aea8818591b' #don't be irresponsible lazy ass and get/use your API key here: https://fixer.io/quickstart
#<<changables


#assemble request link
s_link='http://data.fixer.io/api/' 
s_dateKey='date='
s_date=''
s_access_key='?access_key='+api_key
s_currencies_key='&symbols='
s_currencies=','.join(currencies_list)


#create list of lists for currency storage
n_currencies=len(currencies_list)
d = [[] for reqjson in range(n_currencies)]

check_date = start_date
delta = timedelta(days=1)

#retrieve data in json, store in object, and parse with for loop and put currency data in list of lists
while check_date <= end_date:
    check_date += delta
    s_date = check_date.strftime("%Y-%m-%d")
    apilink=s_link+s_date+s_access_key+s_currencies_key+s_currencies
    req = requests.get(apilink) 
    reqjson = json.loads(req.text, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    ind=0
    for curr in currencies_list:
        d[ind].append(getattr(reqjson.rates, curr))
        ind+=1

#savve raw data
csvRawFileName="From_"+start_date.strftime("%Y-%m-%d")+" to_"+end_date.strftime("%Y-%m-%d")+"Raw.csv"
with open(csvRawFileName, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(d)

#normalize - divide all currencies by the reference currency
for i in range(len(currencies_list)):
    d[i][:] = [j / d[i][(reference_date-start_date).days] for j in d[i]] #current/day_before_first_corona_case
    #d[i][:] = [j / min(d[i]) for j in d[i]] #current/minimum

#savve normalized data
csvNorFileName="From_"+start_date.strftime("%Y-%m-%d")+" to_"+end_date.strftime("%Y-%m-%d")+"Normalized.csv"
with open(csvNorFileName, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(d)


# DRAW

#x axis labels
dates_d=np.arange(start_date,end_date+timedelta(days=1)) 
dates = np.datetime_as_string(dates_d)
fig, ax = plt.subplots()
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
lines = ["-","--","-."]
linecycler = cycle(lines)

#add lists to figure
for i in range(len(currencies_list)):
    if (i==1) : ax.plot(dates, d[i], next(linecycler), linewidth=1, label=currencies_list[i])
    else : ax.plot(dates, d[i], next(linecycler), linewidth=2, label=currencies_list[i])
    plt.xticks(rotation=20, fontsize=5)

#set title
chartTitle='EUR price of DAILY_CURRENCY divided by BEFORE_CORONA_CURRENCY \n from '+start_date.strftime("%Y-%m-%d") + ' to '+end_date.strftime("%Y-%m-%d")
ax.set(xlabel='', ylabel='ratio: currency_day[i]/currency_8.1.2020', title=chartTitle)

ax.grid()
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
ax.legend(fontsize=9, loc='upper center', bbox_to_anchor=(0.5, -0.08),fancybox=False, shadow=False, ncol=7)

#save to file
fileName="From_"+start_date.strftime("%Y-%m-%d")+" to_"+end_date.strftime("%Y-%m-%d")+".png"
fig.savefig(fileName, dpi = 300)
#plt.show()
