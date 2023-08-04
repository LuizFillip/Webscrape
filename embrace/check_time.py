from embrace import URL
from core import request
from embrace_utils import href_attrs
import pandas as pd
import os

def get_deltatime(dat):

    delta = (dat[-1] - dat[0])
    
    args = [int(i) for i in str(delta).split(":")]
    
    return (args[0] + args[1] / 60 + args[2] / 3600)


def get_length(date, 
              inst = "imager", 
              site = "Cariri", 
              ext = "TIF"):
        
    out = []
    for link in request(URL(date, inst = inst, 
                            site = site)):
    
        c = href_attrs()
    
        if ext in link:
            print("getting...", link)
            try:
                out.append(c.iono(link))
            except:
                continue
    
    return len(out)


def quick_look(date):
    return 


def check_year(year, 
               inst, 
               site, 
               ext):
    
    dates = pd.date_range(f"{year}-1-1", 
                          f"{year}-12-31", 
                          freq = "1D")
    
    counts = [get_length(date, 
                         inst = inst, 
                         site = site, 
                         ext = ext)
              for date in dates]
   
    return counts


def count_in_folder(infile, ext = "DVL"):
    
    files = os.listdir(infile)
    
    files = [f for f in files if f.endswith(ext)]
    
    return len(files)


def quick_look(inst = "ionosonde", 
               site = "Fortaleza",
                ext = "DVL", 
                start = 2015, 
                end = 2023, 
                save = True):
    
    rng = list(range(start, end))
    counts = [check_year(year, inst, site, ext)
              for year in rng]
    
    df = pd.DataFrame(counts, 
                      index = rng)
    if save:
        name_to_save = f"{site}_{start}_{end}.txt"
        df.to_csv(name_to_save, index = True, sep = ",")
    
    return df


def main():
    inst = "ionosonde"
    site = "Sao luis"
    df = quick_look(inst, site,
            ext = "DVL", 
            start = 2013, 
            end = 2023)
    
    print(df)