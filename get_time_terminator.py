# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 17:09:23 2022

@author: Luiz
"""

import requests 
from bs4 import BeautifulSoup 
import datetime
import pandas as pd




class get_time_terminator(object):
    
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
        
        url = f"https://www.timeanddate.com/sun/brazil/fortaleza?month={self.month}&year={self.year}"

        r = requests.get(url)
        s = BeautifulSoup(r.text, "html.parser")

        data = s.find_all("table", attrs={'id':'as-monthsun'})

        all_times = {}
        
        for result in data[0].find("tbody"):
            
            day_in = int(result.find('th').text)
            times = result.find_all("td", attrs={'class':['sep c', 
                                                          'c sep', 
                                                          'c sep-l']})

            all_times[day_in] = [ti.text for ti in times[:-1]]
            
        tuples = [("Daylight", "Sunrise"), 	("Daylight", "Sunset"),  
                  ("Astronomical", "start"), ("Astronomical", "end"), 
                  ("Nautical", "start"),	("Nautical", "end"), 
                  ("Civil" , "start"),	("Civil", "end")]
         
        self.df = pd.DataFrame(all_times, 
                               index = tuples).T
        self.df.columns = pd.MultiIndex.from_tuples(self.df.columns, 
                                                    names=[self.year, self.month])   
        
    @property
    def table(self):
        return self.df
    
    def terminator(self, 
                   UT = True, 
                   angle = "Astronomical", 
                   num = 0):
        
        start, end = tuple(self.df.loc[self.df.index == self.day, 
                                  [angle]].values[0])
        
        hour, minute = tuple(end.split(":"))
        
        if UT:
            hour = int(hour) + 3
        else:
            hour = int(hour)

        terminator = datetime.datetime(self.year, 
                                       self.month, 
                                       self.day, 
                                       hour, int(minute))

        return terminator
            
            
            
            
            
            
    
  
