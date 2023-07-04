from embrace import download_one_day
import pandas as pd
import datetime as dt
import os

def download_embrace():
    save_in = "D:\\iono\\2013\\"
    
    
    year = 2013
    dates = pd.date_range(f"{year}-3-16", 
                          f"{year}-3-20", 
                          freq = "1D")
    for date in dates:   
        doy = date.strftime("%j")
        download_one_day(date, 
                         site = "Fortaleza",
                         save_in = save_in, #os.path.join(save_in, doy)
                         ext = ["DVL", "DFT", "SAO", "RSF", "XML"])
        

download_embrace()