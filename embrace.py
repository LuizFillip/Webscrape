# embrace_utils import fname_attrs
from base import request, download
import os
import datetime as dt
import pandas as pd
import pandas as pd

site_code = {
    
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
        site = "Cariri", 
        inst = "imager"):
    
    """
    Build embrace url from date, site 
    for an intrument
    """
    url = "https://embracedata.inpe.br/"
    
    code = site_code[inst][site]
    
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




def filter_hiperlinks(date, 
                   instrument = "imager", 
                   site = "Cariri", 
                   down = False,
                   path_dst = ""):
    
    """Get urls for the date input"""
    
    delta = dt.timedelta(days = 1)
    
    times = pd.date_range(f"{date} 21:00", 
                          f"{date + delta} 07:00", 
                          freq = "10min")
    links = []
    
    for date in [date, date + delta]:
        url = URL(date, instrument = instrument, site = site)
        links.append(request(url))
    
    return links
    


class href_attrs(object):
    
    def __init__(self, file):
        
        self.drift = [ "DVL"] #"SKY", "DFT",
        self.ionog = ["RSF", "SAO", "PNG"]
        
        if any(file.endswith(f) for f in 
               self.drift + self.ionog):
            self.datetime = self.iono(file)
        else:
            pass
            
        
    @staticmethod
    def iono(file):
        
        args = file[:-4].split("_")
    
        year = int(args[1][:4])
        doy = int(args[1][4:7])
        hour = int(args[1][7:9])
        minute = int(args[1][9:11])
        second = int(args[1][11:])
        date = (dt.date(year, 1, 1) + 
                dt.timedelta(doy - 1))
    
        day = date.day
        month = date.month
    
        return dt.datetime(year, 
                           month, 
                           day,
                           hour, 
                           minute, 
                           second)
    

def download_one_day(date, 
                      site = "Sao luis", 
                      inst = "ionosonde", 
                      infile_save = ""):
    url = URL(date, 
              site = site, 
              inst = inst)
    
    links = request(url)
        
    for link in links:
    
        attrs = href_attrs(link)
    
        if any(link.endswith(f) for f in attrs.drift):
            
            print("downloading...", attrs.datetime)
            
            download(url, link, infile_save)

def run_for_all_year(site = "Sao luis", 
                     inst = "ionosonde",
                     year = 2015):
    
    dates = pd.date_range(f"{year}-1-1", 
                          f"{year}-12-31", 
                          freq= "1D")
    

    root = f"D:\\drift\\FZA\\{year}\\"
    
    for date in dates:
        
        doy_str = date.strftime("%j")
        path_to_create = os.path.join(root, doy_str)
        
        try:
            os.mkdir(path_to_create)
        except:
            pass
        
        try:
            download_one_day(date, 
                             site = site, 
                            inst = inst, 
                            infile_save = path_to_create)
        except:
            continue

run_for_all_year(year = 2015)


    
    