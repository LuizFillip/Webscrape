import numpy as np 
import matplotlib.pyplot as plt

import requests 
from bs4 import BeautifulSoup 

import pandas as pd

"""
Web Scrape
* There are many ways to extract useful data from a website - wich is something a lot of us do manually. 
* Web Scraping is way to automate a any process and pull huge amounts of data quickly!
* Web scraping transforms unstructured data from a website into a structured form for you to analyse, This is done using APIs, libraries and writing your own code. 

"""

url = "https://www.worldometers.info/coronavirus/"

r = requests.get(url)
s = BeautifulSoup(r.text, "html.parser")
data = s.find_all("div", class_ = "maincounter-number")


text = ['Cases', 'Deaths', 'Recovered']

for index, name in enumerate(text):
    print("total " + name + ":", data[index].text.strip())
    
data = []

#extract values of 'body' of table
table = s.find('table')
table_body = table.find('tbody')

rows = table_body.find_all('tr')

for row in rows:
    cols = row.find_all('td')
    for td in cols:
        result = td.text
        data.append(result)

#Extract names of table with names of states/country/continent
table_titles = table.find('thead')
titles = table_titles.find_all('th')
titles = [name.text for name in titles] # put in list the names of each columns

cell_text = []

for cell in data:
    cell = cell.strip('\n')
    try:
        val_num = float(cell.replace(',', '')) #convert "number (string)" in float
        cell_text.append(val_num)
    except:
        if cell is None:
            cell_text.append('NaN')
        else:
            cell_text.append(cell) #extract country/continent
final_result = []

#separate in list the values of each rows and your respective columns
n = 13 #number of columns
for index in range(0, len(cell_text), n):
    cell = cell_text[index : index + n]
    final_result.append(cell)
    
df = pd.DataFrame(final_result, columns = titles, index = df['Country,Other'])
#df.index = df['Country,Other']
df