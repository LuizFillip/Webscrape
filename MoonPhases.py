# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 11:49:09 2021

@author: LuizF
"""

import numpy as np 
import datetime
import requests 
from bs4 import BeautifulSoup 
import pandas as pd

year = 2013

#In this code we will we "Time and Date" website for to get
#a table with the moon phases 
url = f'https://www.timeanddate.com/moon/phases/?year={year}'

r = requests.get(url)
s = BeautifulSoup(r.text, "html.parser")
data = s.find_all("table", class_ = "tb-sm zebra fw tb-hover")


table_body = data[0].find_all('tr')

result = []
 
for num in range(len(table_body)):
    
    rows = table_body[num].find_all()

    list_luna = []
    
    result.append(list_luna)
    for elem in rows:
        elem = elem.text
        if elem == '\xa0':
            list_luna.append(np.nan)
        else:
            list_luna.append(elem)
 

def convert_to_datetime(set_date, 
                        year = 2013):
    
    def monthToNum(shortMonth):
        return {
                'jan': 1,
                'fev': 2,
                'mar': 3,
                'abr': 4,
                'mai': 5,
                'jun': 6,
                'jul': 7,
                'ago': 8,
                'set': 9, 
                'out': 10,
                'nov': 11,
                'dez': 12
                }[shortMonth]
    
    def monthToNum2(month_name):
        datetime_object = datetime.datetime.strptime(month_name, "%b")
        return datetime_object.month
    
    if np.nan in set_date:
        return np.nan
    else:    
        day_and_month = set_date[0].split(' de ')
        
        try:
            month = monthToNum2(day_and_month[1])
        except:
            month = monthToNum(day_and_month[1].lower())
            
        #Rearranje os valores do dia, hora e minuto
        day = int(day_and_month[0])
        time = set_date[1].split(':')
        hour = int(time[0])
        minute = int(time[1])
        
        return datetime.datetime(year, month, day, hour, minute)

result = result[:-1]

outside_of_loop = []

for j in range(1, len(result)):
    final_result = []
    outside_of_loop.append(final_result)
    lunation  = result[j][0]
    final_result.append(int(lunation))
    duration = result[j][-1]
    
    setting_datetime = result[j][1:-1]
    
    for i in range(0, len(setting_datetime), 2):
        moon_phase_datetime = convert_to_datetime(setting_datetime[i: i + 2])
    
        final_result.append(moon_phase_datetime)
    
    final_result.append(duration)

df = pd.DataFrame(outside_of_loop, columns = result[0])

df.index = df['Lunation']

del df['Lunation']

