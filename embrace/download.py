from core import request, download
import pandas as pd
import embrace as ec


def daily(dn, 
        site = "Sao luis", 
        inst = "ionosonde", 
        save_in = "", 
        ext = ["DVL"]
        ):
    
    url = ec.URL(dn, site = site, inst = inst)    
    links = request(url)
        
    for link in links:

        if any(f in link for f in ext):
            download(url, link, save_in)
            
    return url


import datetime as dt
    
def main():
    inst = "magnetometer"
    site = "Sao luis"
    dn = dt.date(2013, 12, 29)
    save_in = 'G:/My Drive/Python/data-analysis/database/magnetometers/201303/'
        
    
    daily(dn, 
            site = site, 
            inst = inst, 
            save_in = save_in, 
            ext = ["13m"]
            )

url = "https://embracedata.inpe.br/"
links = request(url)

links