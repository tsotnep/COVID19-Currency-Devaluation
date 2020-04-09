import json
import requests
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import namedtuple
from datetime import date, timedelta, datetime
import csv
import os
from itertools import cycle
import pandas as pd

#changables>>
currencies_list=["USD","GEL","TRY","RUB","AZN","AMD"] #just select any from EurGetRates.py
start_date =     datetime.strptime("2020-01-10","%Y-%m-%d").date()
end_date =       datetime.strptime("2020-04-09","%Y-%m-%d").date()
reference_date = datetime.strptime("2020-01-11","%Y-%m-%d").date()
dirName = 'dataEur' #where previously parsed data json is stored
fileName = '/data_raw.json' #where previously parsed data json is stored
#<<changables


#plot setup
fig, ax = plt.subplots()
dates_d=np.arange(start_date,end_date+timedelta(days=1)) 
dates = np.datetime_as_string(dates_d)
lines = ["-","--","-.",":"]
linecycler = cycle(lines)

#data setup
allData = pd.read_json(dirName+fileName)    #read data
valuesArray = [[] for i in range(len(currencies_list))]
dateArray = []
reference_values = []


for j in range (allData['dataset'].count()):
    data=pd.DataFrame(allData['dataset'][j])    #copy first element
    rates=pd.DataFrame(data['rates'])           #copy rates from first el
    currDate=data['date'][0]                        #read date
    currDateFormatted=datetime.strptime(data['date'][0],"%Y-%m-%d").date()
    if (currDateFormatted >= start_date and currDateFormatted <= end_date):
        rates.reset_index(inplace=True)             #insert new indexes, and move 'currency acronyms' in 'index' column 
        rates.rename(columns={"index":"currName", "rates":"values"}, inplace = True) #rename
        rates.drop(rates.loc[rates['currName'].isin(currencies_list)==False].index, inplace=True) #remove currencies out of our interest
        rates.reset_index(drop=True, inplace=True)  #reset indexes
        dateArray.append(currDate)        
        #make array by currencies
        for i in range(rates['values'].count()):
            valuesArray[i].append(rates['values'][i])
            if (currDateFormatted == reference_date):
                reference_values.append(rates['values'][i])


#divide all by reference currencies
for i in range(len(currencies_list)):
    valuesArray[i][:] = [j / reference_values[i] for j in valuesArray[i]] #current/day_before_first_corona_case

#add to plot
for j in range(rates['currName'].count()):
        if (j%6==0): ax.plot(dateArray, valuesArray[j], marker='o', markersize=3, markevery=3 , markeredgecolor='red', linewidth=1, label=rates['currName'][j])
        if (j%6==1): ax.plot(dateArray, valuesArray[j], marker='^', markersize=3, markevery=5 , markeredgecolor='red', linewidth=1, label=rates['currName'][j])
        if (j%6==2): ax.plot(dateArray, valuesArray[j], marker='*', markersize=3, markevery=7 , markeredgecolor='red', linewidth=1, label=rates['currName'][j])
        if (j%6==3): ax.plot(dateArray, valuesArray[j], marker='s', markersize=3, markevery=11, markeredgecolor='red', linewidth=1, label=rates['currName'][j])
        if (j%6==4): ax.plot(dateArray, valuesArray[j], marker='x', markersize=3, markevery=13, markeredgecolor='red', linewidth=1, label=rates['currName'][j])
        if (j%6==5): ax.plot(dateArray, valuesArray[j], marker='|', markersize=3, markevery=17, markeredgecolor='red', linewidth=1, label=rates['currName'][j])

plt.axvline(reference_date.strftime("%Y-%m-%d"), 0, 1.5, label='reference',color='red')
plt.xticks(rotation=45, fontsize=6)
ax.xaxis.set_major_locator(plt.MaxNLocator(20))
ax.set(xlabel='', ylabel='ratio: currency_day[i]/currency_8.1.2020', title=
'EUR price of DAILY_CURRENCY divided by BEFORE_CORONA_CURRENCY \n from '+start_date.strftime("%Y-%m-%d") + ' to '+end_date.strftime("%Y-%m-%d"))
ax.grid()
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
leg = plt.legend(fontsize=9, loc='upper center', bbox_to_anchor=(0.5, -0.1),fancybox=False, shadow=False, ncol=7, markerscale=2)
leg_lines = leg.get_lines()
plt.setp(leg_lines, linewidth=3)
#ax.legend()

#save to file

plotName="/"+start_date.strftime("%Y-%m-%d")+" "+end_date.strftime("%Y-%m-%d")+", "+str(len(currencies_list))+".png"
fig.savefig(dirName+plotName, dpi = 1500)
#plt.show()


