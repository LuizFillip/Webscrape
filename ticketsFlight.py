# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 19:13:46 2022

@author: LuizF
"""

import requests 
from bs4 import BeautifulSoup 
import pandas as pd

url = "https://www.decolar.com/shop/flights/results/oneway/CPV/SAO/2022-06-10/1/0/0/NA/NA/NA/NA?from=SB&di=1-0"

r = requests.get(url)
s = BeautifulSoup(r.text, "html.parser")
spans = s.find_all('span') #{"class" : "btn-text"})

# create a list of lines corresponding to element texts
#lines = [span.get_text() for span in spans]

print(spans.get_text())