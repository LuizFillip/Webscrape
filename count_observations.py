from EMBRACE_Data_Download import URL
import requests 
from bs4 import BeautifulSoup 
import datetime 

from image_utils import imager_fname
year = 2014
doy = datetime.date(year, 5, 24).timetuple().tm_yday  



def quick_look(date, doy = None, 
               instrument = "imager", 
               site = "Sao Joao do Cariri", 
               condition = "O6"):
    
    url = URL(year, doy, 
                    instrument = instrument, 
                    site = site)
    r = requests.get(url)
    s = BeautifulSoup(r.text, "html.parser")
    
    parser = s.find_all('a', href = True)
    
    
    
    out_date = []
    for link in parser:
        
        href = link['href']
    
        if condition in href:
            out_date.append(imager_fname(href).datetime)
            
    return out_date