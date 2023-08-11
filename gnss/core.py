import os
import Webscrape as wb
import zipfile
from unlzw3 import unlzw
from GNSS import paths
from base import make_dir

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
        stations = None
        ):
    url = wb.rinex_url(year, doy)
    
    path_to_save = paths(year, doy, root = root).rinex     
    path_to_save = make_dir(path_to_save)
    
    if stations is not None:
        receivers_list = wb.filter_rinex(
            url, sel_stations = stations
            )
    else:
        receivers_list = wb.request(url)
        
    out = []
    
    for href in receivers_list:
        
        if '.zip' in href:
        
            files = wb.download(url, href, path_to_save)
            out.append(files)
            try:
                unzip_rinex(files, year, path_to_save)
            except:
                continue
           
    return out



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
    
    
def folders_orbits(year, root = 'D:\\'):
    for const in ["igl", "igr"]:
        make_dir(paths(year, root = root).orbit_base)
        
        path_to_save = paths(
            year, 0, 
            root = root).orbit(const = const)
        
        make_dir(path_to_save)
   
    
def download_orbit(
        year: int, 
        doy: int, 
        root: str = "D:\\",
        constellations = ["igl", "igr"], 
        net = 'igs'
        ):
    

    for i, const in enumerate(constellations):
        fname, url = wb.orbit_url(
            year, doy, 
            network = net, 
            const = const
            )
    
        path_to_save = paths(
            year, doy, 
            root = root).orbit(const = const)
        
        for href in wb.request(url):
            if fname in href:
                files = wb.download(url, href, path_to_save)
                unzip_orbit(files)
                
            
def download_one_year(year, 
                      start: int = 1, 
                      end: int = 366, 
                      root: str = "D:\\", 
                      rinex = True):
    
    
    """Download rinex and orbit files for whole year"""
    
    for doy in range(start, end, 1):
       
        download_orbit(
            year, 
            doy, 
            root = root
            )
            

    # wb.make_dir(path_to_save)
        
def main():
    year = 2019
    # for const in ['igr', 'igl']:
    const = 'igl'
    times = wb.missing_times(year, const)
    
    for dn in times:
        download_orbit(
            year, 
            dn.day_of_year, 
            constellations = [const],
            root = "D:\\"
            )
        
main()