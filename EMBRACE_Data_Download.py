import requests 
from tqdm import tqdm
from bs4 import BeautifulSoup 
import time
import os
import datetime
import pandas as pd
import shutil

infos = {
    
         "ionosonde": {"Fortaleza": "FZA0M", 
                       "Sao luis": "SAA0K", 
                       "Belem": "BLJ03"}, 
         
         "imager": {"Cariri": "CA", 
                    "Bom Jesus da Lapa" : "BJL", 
                    "Cachoeira Paulista": "CP"} 
         }


class date_from_filename(object):
    
    """Convert digisonde, imager and TEC files filename (EMBRACE format) to datetime"""
    
    def __init__(self, file):
        
        extension = file[-4:]
        args = file[:-4].split("_")
        
        if ((extension == ".SAO") or 
            (extension == ".RSF")):
            
            
            year = int(args[1][:4])
            doy = int(args[1][4:7])
            hour = int(args[1][7:9])
            minute = int(args[1][9:11])
            
            date = datetime.date(year, 1, 1) + datetime.timedelta(doy - 1)
        
            day = date.day
            month = date.month
        
            self.datetime = datetime.datetime(year, month, day,
                                              hour, minute)
            
        elif ((extension == ".png") or
              (extension == ".tif")):
            
            args = file[:-4].split("_")
            
            date = args[2]
            time = args[3]
            self.datetime = datetime.datetime.strptime(date + time, 
                                                       "%Y%m%d%H%M%S")
            
        elif ((extension == ".txt") or 
             ("TECMAP" in file)):
            
            args = file[:-4].split("_")
            
            date = args[1]
            time = args[2]
            self.datetime = datetime.datetime.strptime(date + time, 
                                                       "%Y%m%d%H%M%S")
    
        

def copy_tec_files(date, infile = "G:\\My Drive\\TEC_2014\\", path_to_save = ""):
    
    delta = datetime.timedelta(days = 1)
    
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
                
                ref_time = date_from_filename(filename).datetime
                
                if (ref_time >= times[0]) and (ref_time <= times[-1]):
                    path_src = os.path.join(infile, folder, filename)
                    path_dst = os.path.join(path_to_save, filename)
                    try:
                        shutil.copy2(path_src, path_dst)
                    except:
                        print("doesn cant copy the files")
def URL(date, 
        year = 2014, 
        doy = 1, 
        instrument = "imager", 
        site = "Cariri"):
    
    if date == None:
        date = datetime.date(year, 1, 1) + datetime.timedelta(doy - 1)
    
    """Build embrace data download from day and year"""
    url = "https://embracedata.inpe.br/"
    
    code = infos[instrument][site]
    
    str_doy = date.strftime("%j")
    str_mon = date.strftime("%m")
    str_day = date.strftime("%d")
    
    if instrument == "imager":
        url += f"{instrument}/{code}/{year}/{code}_{year}_{str_mon}{str_day}/"
        
    elif instrument == "ionosonde":
        url += f"{instrument}/{code}/{year}/{str_doy}/"
    
    return url


def request(url, times):
    r = requests.get(url)
    s = BeautifulSoup(r.text, "html.parser")
 
    parser = s.find_all('a', href = True)
    
    out_href = []
    
    for link in parser:
        href = link['href']
        
        if "imager" in url:
            cond = ["O6" in href, 
                    "DARK" not in href]

        elif "ionosonde" in url:
            cond = [".RSF" in href]
            
        if all(cond):
            ref_time = date_from_filename(href).datetime
            if (ref_time >= times[0]) and (ref_time <= times[-1]):
                out_href.append(href)
                
    return out_href

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

    


def download(url, href, path_to_save = ""):
    
    """Use request for download the data"""
    
    remote_file = requests.get(url + href)
    total_length = int(remote_file.headers.get('content-length', 0))

    out_file = os.path.join(path_to_save, href)
    
    with open(out_file, 'wb') as f:
        for chunk in remote_file.iter_content(chunk_size =  1024): 
            if chunk: 
                f.write(chunk) 
                
    return out_file


def make_dir(date, root = ""):
    """Create a new directory by path must be there year and doy"""
    doy_str = date.strftime("%j")
    
    path_to_create = os.path.join(root, doy_str)
    
    
    try:
        os.mkdir(path_to_create)
        
        for subfolder in ["imager", "ionosonde", "tec"]:   
            os.makedirs(os.path.join(path_to_create, subfolder)) 
        
            print(f"Creation of the directory {subfolder} successfully")
        
    except OSError:
        print(f"Creation of the directory {path_to_create} failed")
      
   
    return path_to_create




def tri_download(date, root, tec_infile = "G:\\My Drive\\TEC_2014\\"):

    path = make_dir(date, root = root)
    
    
    for instrument, site in zip(["imager", "ionosonde"], 
                               ["Cariri", "Fortaleza"]):
        
    
        get_hiperlinks(date, instrument = instrument, 
                       site = site, path_dst = path, down = True)
        
        
        copy_tec_files(date, infile = tec_infile, 
                       path_to_save = os.path.join(path, "tec"))
        
obs = ['24/01/2014', '29/01/2014', '24/02/2014', '26/02/2014', 
         '25/03/2014', '29/03/2014', '19/04/2014', '23/04/2014', 
         '19/05/2014', '23/05/2014', '21/06/2014', '29/06/2014', 
         '03/07/2014', '04/07/2014', '13/08/2014', '14/08/2014', 
         '17/08/2014', '13/09/2014', '14/09/2014', '17/10/2014', 
         '23/10/2014', '21/11/2014', '15/11/2014', '19/12/2014', 
         '21/12/2014']       


date = datetime.date(2014, 6, 21)


obs = ['01/01/2014', '21/06/2014', '23/10/2014']

root = "D:\\"


tecinfile = "D:\\database\\instr\\TEC_2014\\"




for date in pd.to_datetime(obs):
    tri_download(date, root, tec_infile = tecinfile)

