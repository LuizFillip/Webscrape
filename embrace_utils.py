import datetime as dt
import os
import pandas as pd
from embrace import URL
import shutil 
from base import request


site_codes = {
    
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


            
def copy_tec_files(date, 
                   infile = "G:\\My Drive\\TEC_2014\\", 
                   path_to_save = ""):
    
    delta =  dt.timedelta(days = 1)
    
    times = pd.date_range(f"{date} 21:00", 
                          f"{date + delta} 07:00", 
                          freq = "10min")
    
    _, folders, _ = next(os.walk(infile))

    str_mon = date.strftime("%m")

    def split_folder(folder):
        args = folder.split("_")
        year = args[1]
        mon = args[2]
        return year, mon

    for folder in folders:
        year, mon = split_folder(folder)
        
        if mon == str_mon:
            _, _, files = next(os.walk(infile + folder))
            
            for filename in files:
                
                ref_time = href_attrs(filename).datetime
                
                if (ref_time >= times[0]) and (ref_time <= times[-1]):
                    path_src = os.path.join(infile, folder, filename)
                    path_dst = os.path.join(path_to_save, filename)
                    try:
                        shutil.copy2(path_src, path_dst)
                    except:
                        print("doesn cant copy the files")

class href_attrs(object):
    
       
    """Convert digisonde, imager and TEC files 
    filename (EMBRACE format) to datetime"""
    
    def __init__(self, file):
        
        self.drift = [ "DVL", "SKY", "DFT"]
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
    
    @staticmethod
    def imag(file):
        args = file[:-4].split("_")
        date = args[2]
        time = args[3]
        return dt.datetime.strptime(date + time, 
                                    "%Y%m%d%H%M%S")
    
    @staticmethod
    def tec(file):
        args = file[:-4].split("_")
        
        date = args[1]
        time = args[2]
        return dt.datetime.strptime(date + time, 
                                     "%Y%m%d%H%M%S")
    
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
        url = URL(date, 
                  instrument = instrument, 
                  site = site)
        links.append(request(url))
    
    return links   
    
def filter_links(url, times, date):
    
    links = request(URL(date))
    
    out_href = []

    for href in links:
        
        if "imager" in url:
            cond = ["O6" in href, "DARK" not in href]
        elif "ionosonde" in url:
            
            cond = [".RSF" in href]
            
        if all(cond):
            ref_time = date_from_filename(href).datetime
            if (ref_time >= times[0]) and (ref_time <= times[-1]):
                out_href.append(href)
    return out_href
            
            

