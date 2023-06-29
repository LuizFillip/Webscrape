from embrace_utils import site_codes
from core import request, download
import os
import pandas as pd
import datetime as dt

def URL(date, 
        site = "Cariri", 
        inst = "imager"):
    
    """
    Build embrace url from date, site 
    for an intrument
    """
    url = "https://embracedata.inpe.br/"
    
    code = site_codes[inst][site]
    
    year = date.year
    str_doy = date.strftime("%j")
    str_mon = date.strftime("%m")
    str_day = date.strftime("%d")
    
    url += f"{inst}/{code}/{year}/"
    
    if inst == "imager":
        url += f"{code}_{year}_{str_mon}{str_day}/"
        
    elif inst == "ionosonde":
        url += f"{str_doy}/"
        
    elif inst == "magnetometer":
        url +=  f"{code}/" # NOT COMPLETED
    
    return url

    
def download_one_day(date, 
                      site = "Sao luis", 
                      inst = "ionosonde", 
                      save_in = "", 
                      ext = ["DVL"]):
    url = URL(date, 
              site = site, 
              inst = inst)
    
    links = request(url)
        
    for link in links:

        if any(f in link for f in ext):
            download(url, link, save_in)
            
    return url

def download_one_year(inst, site, year, root):
    
    d = build_dir(inst, site, year, root)

    d.site_path
    d.year_path

    dates = pd.date_range(f"{year}-1-1", 
                          f"{year}-12-31", 
                          freq = "1D")
    for date in dates:    
        doy_str = date.strftime("%j")
        save_in = d.doy_path(doy_str)
         
        try:

            download_one_day(
                date, 
                site = site, 
                inst = inst, 
                save_in = save_in)
        except:
            continue




    
   
def main():

    inst = "magnetometer"
    site = "Sao luis"
    date = dt.date(2013, 12, 29)
    url = URL(date, 
              site = site, 
              inst = inst)
    
    links = request(url)
    
    print(links)
    

main()