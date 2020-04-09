import json
import requests
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from collections import namedtuple
from datetime import date, timedelta
from matplotlib.ticker import MaxNLocator
import csv
import os
from itertools import cycle
import pandas as pd

#changables>>
currencies_list=["USD","GEL","PLN"] #just select any from EurGetRates.py
start_date = date(2018, 1, 1)
end_date = date(2020, 4, 9)
reference_date = date(2020, 4, 9)
dirName = 'dataEur' #where previously parsed data json is stored
fileName = '/data_raw2.json' #where previously parsed data json is stored
#<<changables

allData = pd.read_json(dirName+fileName)    #read data
data=pd.DataFrame(allData['dataset'][0])    #copy first element
rates=pd.DataFrame(data['rates'])           #copy rates from first el
date=data['date'][0]                        #read date

rates.reset_index(inplace=True)             #insert new indexes, and move 'currency acronyms' in 'index' column 
rates.rename(columns={"index":"currency"}, inplace = True) #rename
rates.drop(rates.loc[rates['currency'].isin(currencies_list)==False].index, inplace=True) #remove currencies out of our interest
rates.reset_index(drop=True, inplace=True)  #reset indexes
print(rates)


# DRAW
fig, ax = plt.subplots()

dates_d=np.arange(start_date,end_date+timedelta(days=1)) 
dates = np.datetime_as_string(dates_d)

lines = ["-","--","-."]
linecycler = cycle(lines)

#add lists to figure
for i in range(rates['currency'].count()):
    ax.plot(dates, rates[i]['rates'], next(linecycler), linewidth=1, label=rates[i]['currency'])

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
