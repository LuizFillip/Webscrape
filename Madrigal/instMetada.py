# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 14:44:53 2022

@author: LuizF
"""

import requests 
from bs4 import BeautifulSoup 
import pandas as pd

url = "http://cedar.openmadrigal.org/instMetadata"

r = requests.get(url)
s = BeautifulSoup(r.text, "html.parser")
#data = s.find_all("div", class_ = "maincounter-number")


data = []

#extract values of 'body' of table
table = s.find('table')
table_body = table.find('tbody')

rows = table_body.find_all('tr')

for row in rows:
    cols = row.find_all('td')
    extract_row = []
    data.append(extract_row)
    for td in cols:
  
        extract_row.append(td.text)
        
table_titles = table.find('thead')
titles = [name.text for name in table_titles.find_all('th')] 
        
df = pd.DataFrame(data, columns = titles)

print(df.loc[df['Category'] == 'Fabry-Perots',  
             ['Name', 'Latitude', 'Longitude (-180-180)']])