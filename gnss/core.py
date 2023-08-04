import os
import gnss as g
import zipfile
from unlzw3 import unlzw
import time
from core import request, download



def unzip_rinex(
        files:str, 
        year:int, 
        path_to_save:str
        ) -> None:
    
    zip_path = os.path.join(path_to_save, files)
    zip_file = zipfile.ZipFile(zip_path, 'r') 
    ext_year = str(year)[-2:] 
    
    extensions = [f"{ext_year}o", f"{ext_year}d"]
    
    zip_file = zipfile.ZipFile(zip_path, 'r') 
    
    for file in zip_file.namelist():
        
        if any(file.endswith(ext) for ext in extensions):
            
            zip_file.extract(file, path_to_save)
            
    zip_file.close()
    os.remove(zip_path)
    
            

def download_rinex(
        year, 
        doy, 
        root = "D:\\",
        filter_stations = True
        ):
    url = g.rinex_url(year, doy)
    
    path_to_save = g.paths(year, doy, root = root).rinex     
    path_to_save = g.make_dir(path_to_save)
    
    if filter_stations:
        receivers_list = g.filter_rinex(url)
    else:
        receivers_list = request(url)
    
    for href in receivers_list:
        
        files = download(url, href, path_to_save)
        unzip_rinex(files, year, path_to_save)
        
   
def unzip_orbit(files): 
    fh = open(files, 'rb')
    compressed_data = fh.read()
    uncompressed_data = unlzw(compressed_data)
    
    str_mybytes = str(uncompressed_data)
    
    again_mybytes = eval(str_mybytes)
    decoded = again_mybytes.decode('utf8')
    
    file = open(files.replace(".Z", ""), 'w')
    file.write(decoded)
    file.close()
    fh.close()
    os.remove(files)
   
    
def download_orbit(
        year: int, 
        doy: int, 
        root: str = "D:\\",
        constellations = ["igl", "igr"], 
        network = 'igs2'
        ):
    
    
    for const in constellations:
        fname, url = g.orbit_url(
            year, doy, 
            network = "igs2", 
            const = const
            )
    
        path_to_save = g.paths(year, doy, 
                             root = root).orbit(const = const)
        
        for href in request(url):
            if fname in href:
                files = download(url, href, path_to_save)
                unzip_orbit(files)
                
            
def download_one_year(year, 
                      start: int = 1, 
                      end: int = 366, 
                      root: str = "D:\\", 
                      rinex = True):
    
    
    """Download rinex and orbit files for whole year"""
    
    for doy in range(start, end, 1):
       
        try:
            if rinex:
                download_rinex(
                    year, 
                    doy, 
                    root = root
                    )
            else:
                download_orbit(
                    year, 
                    doy, 
                    root = root
                    )
                               
        except:
            print("it was not possible download...", 
                  g.date_from_doy(year, doy))
            continue
            

def main():
    
  
    
    year = 2013
    start_time = time.time()
    
    download_one_year(year, rinex = False)
    
    
    print("--- %s minutes ---" % ((time.time() - start_time) / 3600))
    


    # filename, url = orbit_url(2014, 105, network = "igs2", const = "igl")
    
    # # url = "https://files.igs.org/pub/glonass/products/1721/"
    # # print(request(url))
    
    year = 2014
    root = "D:\\"
    for doy in range(1, 366):
        # fname, url = orbit_url(2014, doy, network = "igs2", const = "igl")
        
        download_orbit(
            year, 
            doy, 
            root = root,
        constellations=['igl']
        )





