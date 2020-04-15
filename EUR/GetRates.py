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

#changables>>
currencies_list=["USD","GEL","RUB","PLN","RON","UAH","TRY","GBP","RON","CAD","AED","AMD","AZN","IRR","MXN","YER","XAU","XAG","VND","SEK","SAR","QAR","NOK","MDL","KZT","LKR","KWD","KRW","JPY","INR","HUF","ILS","HUF","HRK","HKD","GBP","EGP","CZK","CNY","CHF","BYR","BTC","BGN","ARS"] #just add any if available : https://fixer.io/symbols
#start_date = date(2013, 1, 1) #json already contains data starting from 2013.1.1, if you retrieve data before that date, insert it inside json before that date also, do not append
start_date = date(2020, 4, 7) #you can simply specify new dates and run the code, it will it append to existing json file
end_date = date(2020, 4, 14) #should not be more than 1000 days difference (api limits)
api_key = 'ccd706e810a40c70ad672096375e5ad5' #don't be irresponsible lazy ass and get/use your API key here: https://fixer.io/quickstart
dirName = 'dataEur' #where generated data will be stored
fileName = '/data_raw.json' #where generated data will be stored
#<<changables

#98937b3cb98e0848a416409533b38530
#39aa3e24eaf900af8a4f6f3ca07ae530


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

path=dirName+fileName
if (os.path.exists(path)):
    lines = open(path, 'r').readlines()
    lines = lines[:-1]
    open(path, 'w').writelines(lines) 
    open(path, 'a').writelines("},")
    fileJson = open(path, "a")
else:
    os.makedirs(dirName, exist_ok=True)
    fileJson = open(path, "w")
    fileJson.write('{\"dataset\":[')

while check_date <= end_date:
    check_date += delta
    s_date = check_date.strftime("%Y-%m-%d")
    apilink=s_link+s_date+s_access_key+s_currencies_key+s_currencies
    req = requests.get(apilink) 
    reqJson = json.loads(req.text)
    reqJsonPretty = json.dumps(reqJson,indent=4)
    fileJson.write(reqJsonPretty)
    fileJson.write(',')

#removing last comma
fileJson.close()
lines = open(path, 'r').readlines()
lines = lines[:-1]
open(path, 'w').writelines(lines) 

#finish json dt packeet
open(path, 'a').writelines("}]}") 
