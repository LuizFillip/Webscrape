from embrace import URL
from core import request
import datetime as dt
from embrace_utils import href_attrs
import pandas as pd

def get_deltatime(dat):

    delta = (dat[-1] - dat[0])
    
    args = [int(i) for i in str(delta).split(":")]
    
    return (args[0] + args[1] / 60 + args[2] / 3600)


def get_length(date, 
              inst = "imager", 
              site = "Cariri", 
              ext = "TIF"):
        
    out = []
    for link in request(URL(date,
                            inst = inst, 
                            site = site)):
    
        c = href_attrs()
    
        if ext in link:
            try:
                out.append(c.iono(link))
            except:
                continue
    
    return len(out)


def quick_look(date, 
               ):
     
    return 


ends = {"ionosonde":  {"drift": ["DVL", "SKY", "DFT"], 
                        "SAO": ["RSF", "SAO", "PNG"], 
                        }
        }

year = 2015
def check_year(year, 
               inst, 
               site, 
               ext):
    
    dates = pd.date_range(f"{year}-1-1", 
                          f"{year}-12-31", 
                          freq = "1D")
    
    number = []
    for date in dates:
        number.append(get_length(date, 
                      inst = inst, 
                      site = site, 
                      ext = ext))
    return number
    
    
#%%
import matplotlib.pyplot as plt
inst = "ionosonde"
site = "Fortaleza"
ext = "DVL"
