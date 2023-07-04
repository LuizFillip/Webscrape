from core import request, download
import pandas as pd
import embrace as ec


def daily(date, 
        site = "Sao luis", 
        inst = "ionosonde", 
        save_in = "", 
        ext = ["DVL"]
        ):
    
    
    url = ec.URL(date, 
              site = site, 
              inst = inst)
    
    links = request(url)
        
    for link in links:

        if any(f in link for f in ext):
            download(url, link, save_in)
            
    return url

def yearly(inst, site, year, root):
    
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

            daily(
                date, 
                site = site, 
                inst = inst, 
                save_in = save_in)
        except:
            continue

import datetime as dt
    

inst = "magnetometer"
site = "Sao luis"
dn = dt.date(2013, 12, 29)

url = ec.URL(dn, site = site, inst = inst)
    

# daily(dn, 
#         site = site, 
#         inst = inst, 
#         save_in = "", 
#         ext = ["DVL"]
#         )
# url = ''
# links = request(url)

# links
import requests
requests.get(url, verify=False)