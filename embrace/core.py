from embrace_utils import href_attrs, site_codes
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



class build_dir(object):
    
    """
    Create directories from input names:
        inst: intrumentation type (e.g. imager)
        site: site location for each inst.
        year: observation year
        root: path root
    """
    
    def __init__(
            self, inst, site, year, root,
             ):
  
        self.root = str(root)
        self.year = str(year)
        self.name_dir = site_codes[inst][site][:3]
        
    @staticmethod
    def create_dir(path):
        try:
            os.mkdir(path)
        except OSError:
            print(f"{path} wasn`t created")         
        return path
        
    @property  
    def site_path(self):
        return self.create_dir(
                    os.path.join(
                    self.root, 
                    self.name_dir))
        
    @property
    def year_path(self): 
        return self.create_dir(
                    os.path.join(
                    self.root, 
                    self.name_dir, 
                    self.year))
    
    def doy_path(self, doy): 
        return self.create_dir(
                    os.path.join(
                    self.root, 
                    self.name_dir, 
                    self.year, 
                    str(doy)))
    
   
def main():

    #root = "D:\\drift\\"
    #root = str(Path.cwd())
    inst = "ionosonde"
    site = "Cachoeira"
    date = dt.date(2015, 3, 1)
    url = URL(date, 
              site = site, 
              inst = inst)
    
    links = request(url)
    
    print(links)
    

#main()
        