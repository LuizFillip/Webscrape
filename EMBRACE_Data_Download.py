from common import request, download
from base import date_from_filename
import os
import datetime
import pandas as pd

infos = {
    
         "ionosonde": {"Fortaleza": "FZA0M", 
                       "Sao luis": "SAA0K", 
                       "Belem": "BLJ03", 
                       "Cachoeira": "CAJ2M", 
                       "Santa Maria": "SMK29", 
                       "Boa Vista": "BVJ03", 
                       "Campo Grande": "CGK21"}, 
         
         "imager": {"Cariri": "CA", 
                    "Bom Jesus da Lapa" : "BJL", 
                    "Cachoeira Paulista": "CP", 
                    "Comandante Ferraz": "CF", 
                    "Sao Martinho da Serra": "SMS"} 
         }




def URL(date, 
        instrument = "imager", 
        site = "Cariri"):
    
    """Build embrace data download from day and year"""
    url = "https://embracedata.inpe.br/"
    
    code = infos[instrument][site]
    
    year = date.year
    str_doy = date.strftime("%j")
    str_mon = date.strftime("%m")
    str_day = date.strftime("%d")
    
    if instrument == "imager":
        url += f"{instrument}/{code}/{year}/{code}_{year}_{str_mon}{str_day}/"
        
    elif instrument == "ionosonde":
        url += f"{instrument}/{code}/{year}/{str_doy}/"
    
    return url




def get_hiperlinks(date, 
                   instrument = "imager", 
                   site = "Cariri", 
                   down = False,
                   path_dst = ""):
    
    """Get urls for the date input"""
    
    delta = datetime.timedelta(days = 1)
    
    times = pd.date_range(f"{date} 21:00", 
                          f"{date + delta} 07:00", 
                          freq = "10min")
    
    for date in [date, date + delta]:
        url = URL(date, instrument = instrument, site = site)
        links = request(url, times)
    
        if down:
            for link in links:
                print("downloading...", link)
                download(url, link, path_to_save = os.path.join(path_dst, 
                                                     instrument))

    


def filter_links():
    
    links = request(URL(date))


    for link in links:
        
    if "imager" in url:
        cond = ["O6" in href, "DARK" not in href]

    elif "ionosonde" in url:
        
        cond = [".RSF" in href]
        
    if all(cond):
        ref_time = date_from_filename(href).datetime
        if (ref_time >= times[0]) and (ref_time <= times[-1]):
            out_href.append(href)
            
            
date = datetime.date(2014, 1, 3)



    
    





