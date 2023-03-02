from embrace import download_one_day
import pandas as pd
import datetime as dt



save_in = "D:\\drift\\CAJ\\2015\\"


year = 2015
site = "Cachoeira"
inst = "ionosonde"
dates = pd.date_range(f"{year}-1-1", 
                      f"{year}-12-31", 
                      freq = "1D")
for date in dates:    
    try:

       download_one_day(date, 
                       site = site, 
                       inst = inst, 
                       save_in = save_in, 
                       ext = ["DVL", "DFT"])
    except:
        continue
    
