import json
import requests
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
from collections import namedtuple
from datetime import date, timedelta, datetime
import csv
import os
from itertools import cycle
import pandas as pd
import math

#changables>>
currencies_list=["GEL",'AMD','TYR','AZN','RUB','USD'] #just select any from EurGetRates.py
start_date =     datetime.strptime("2020-01-01","%Y-%m-%d").date() #min: 2013, 01, 01
end_date =       datetime.strptime("2020-04-14","%Y-%m-%d").date() #max: 2020, 04, 09
reference_date = datetime.strptime("2020-01-02","%Y-%m-%d").date() #should be > min
dirName = 'dataEur' #where previously parsed data json is stored
fileName = '/data_raw.json' #where previously parsed data json is stored
drawPercentages = True
#<<changables


#plot setup
fig, ax = plt.subplots()
dates_d=np.arange(start_date,end_date+timedelta(days=1)) 
dates = np.datetime_as_string(dates_d)
lines = ["-","--","-.",":"]
linecycler = cycle(lines)

#data setup
df = pd.read_json(dirName+fileName)    #read data

valuesArray = [[] for i in range(len(currencies_list))]
dateArray = []
reference_values = []


for j in range (df['dataset'].count()):
    data=pd.DataFrame(df['dataset'][j])    #copy first element
    rates=pd.DataFrame(data['rates'])           #copy rates from first el
    currDate=data['date'][0]                        #read date
    currDateFormatted=datetime.strptime(data['date'][0],"%Y-%m-%d").date()

    #check if its in the requested range
    if (currDateFormatted >= start_date and currDateFormatted <= end_date and dateArray.count(currDate)==0): #it skips duplicate dates, but, it never sorts values by date, keep that in mind(dont append older days, if those days didn't exist in the list before)
        rates_indexed=rates.reset_index()             #insert new indexes, and move 'currency acronyms' in 'index' column 
        rates_indexed.rename(columns={"index":"currName", "rates":"values"}, inplace = True) #rename
        rates_indexed.drop(rates_indexed.loc[rates_indexed['currName'].isin(currencies_list)==False].index, inplace=True) #remove currencies out of our interest
        rates_indexed.reset_index(drop=True, inplace=True)  #renumber indexes
        dateArray.append(currDate) 
               
        #make array by currencies
        for i in range(rates_indexed['values'].count()):
            if (rates_indexed['currName'][i]=='GEL' and rates_indexed['values'][i]>300):
                valuesArray[i].append(3.03150027) #on date: 2018.12.18, GEL value has a typo, it's 303.150027 instead of 3.03150027
            else :
                valuesArray[i].append(rates_indexed['values'][i])
            if (drawPercentages and currDateFormatted == reference_date):
                reference_values.append(rates_indexed['values'][i])
if (drawPercentages):
    #divide all by reference currencies
    for i in range(len(currencies_list)):
        valuesArray[i][:] = [(j / reference_values[i])*100-100 for j in valuesArray[i]] #current/day_before_first_corona_case

totalDays = len(valuesArray[0])
#add to plot
for j in range(rates_indexed['currName'].count()):
        if (j%6==0): ax.plot(dateArray, valuesArray[j], marker='o', markersize=3, markevery=math.ceil(totalDays/9), markeredgecolor='red', linewidth=1, label=rates_indexed['currName'][j])
        if (j%6==1): ax.plot(dateArray, valuesArray[j], marker='^', markersize=3, markevery=math.ceil(totalDays/11) , markeredgecolor='red', linewidth=1, label=rates_indexed['currName'][j])
        if (j%6==2): ax.plot(dateArray, valuesArray[j], marker='*', markersize=3, markevery=math.ceil(totalDays/13) , markeredgecolor='red', linewidth=1, label=rates_indexed['currName'][j])
        if (j%6==3): ax.plot(dateArray, valuesArray[j], marker='s', markersize=3, markevery=math.ceil(totalDays/15), markeredgecolor='red', linewidth=1, label=rates_indexed['currName'][j])
        if (j%6==4): ax.plot(dateArray, valuesArray[j], marker='x', markersize=3, markevery=math.ceil(totalDays/5), markeredgecolor='red', linewidth=1, label=rates_indexed['currName'][j])
        if (j%6==5): ax.plot(dateArray, valuesArray[j], marker='|', markersize=3, markevery=math.ceil(totalDays/7), markeredgecolor='red', linewidth=1, label=rates_indexed['currName'][j])

if (drawPercentages): plt.axvline(reference_date.strftime("%Y-%m-%d"), 0, 1.5, label='reference',color='red')
plt.xticks(rotation=45, fontsize=6)
if (totalDays > 20): ax.xaxis.set_major_locator(plt.MaxNLocator(20))
else: ax.xaxis.set_major_locator(plt.MaxNLocator(totalDays))
ylabeltext='devaluation in %' if (drawPercentages) else 'price for 1 euro'
ax.set(xlabel='', ylabel=ylabeltext, title='devaluation of currencies to EUR \n '+start_date.strftime("%Y.%m.%d") + ' - '+end_date.strftime("%Y.%m.%d"))
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


