from core import request, download
import pandas as pd
import embrace as ec


def daily(dn, 
        site = "Sao luis", 
        inst = "ionosonde", 
        save_in = "", 
        ext = ["DVL", 'SAO', 'RSF']
        ):
    
    url = ec.URL(dn, site = site, inst = inst)    
    links = request(url)
        
    for link in links:

        if any(f in link for f in ext):
            download(url, link, save_in)
            
    return url
    
def run_years():
    for year in range(2017, 2023):
        dates = pd.date_range(f'{year}-01-01', 
                              f'{year}-12-31', 
                              freq = '1D')
        save_in = f'D:\\drift\\SAA\\{year}\\'
        for dn in dates:
            try:
                print(dn)
                
                daily(dn, 
                        save_in = save_in
                        )
            except:
                continue