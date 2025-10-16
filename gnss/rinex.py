import Webscrape as wb
import GNSS as gs
import base as b 
import os
from tqdm import tqdm 

PATH_CHILE = 'D:\\database\\GNSS\\rinex\\chile\\'

networks = {
    "ibge" : 'https://geoftp.ibge.gov.br/informacoes_sobre_posicionamento_geodesico/rbmc/dados', 
    'igs': 'https://igs.bkg.bund.de/root_ftp/IGS/obs/',
    'chile': 'http://gps.csn.uchile.cl/data/', 
    'lisn': 'http://lisn.igp.gob.pe/jdata/database/gps/rinex/',
    'gage': 'https://gage-data.earthscope.org/archive/gnss/rinex/obs/',
    'garner': 'http://garner.ucsd.edu/pub/rinex/'
    }


def rinex_url(year, doy, network = "ibge"):
    date = gs.date_from_doy(year, doy)
    doy_str = date.strftime("%j")
    return f"{networks[network]}/{year}/{doy_str}/"

def rinex3_fname(dn):
    doy = dn.strftime('%j')
    year = dn.year
    doy = dn.timetuple().tm_yday
    week, number = gs.gpsweek_from_doy_and_year(year, doy)
    
    url = networks['igs'] + f'{week}/'
    
    return url, f'IGS0OPSFIN_{year}{doy}0000_01D_15M_ORB.SP3.gz'




def filter_rinex(url: str, 
        sel_stations: list[str]
        ):
    
  out = []
  for href in wb.request(url):
      
      rules = [f in href for f in sel_stations]
      if any(rules):
          out.append(href)
          
  return out




def download_rinex(
        year, 
        doy,
        path_to_save,
        stations = None,
        network = 'ibge', 
        
        ):

    url = rinex_url(year, doy, network)
    io = 'downloading'
    for href in tqdm(wb.request(url), io):
     
        if any([z in href for z in stations]):
            
            ends = ['.zip', 'd.Z', 'crx.gz']
            if any([href.endswith(e) for e in ends]):
             
               wb.download(
                   url, 
                   href, 
                   path_to_save
                   )
           
    return None



def uncompress(path_root):
    unzip_msg = 'unzipping'
    
    files = []
    for sts in tqdm(os.listdir(path_root), unzip_msg):
        path_in = os.path.join(path_root, sts)
        
        if sts.endswith('Z'):
           
            try:
                wb.unzip_Z(path_in)
                files.append(sts)
                
            except:
                continue
            
        elif sts.endswith('zip'):
         
            try:
                wb.unzip_zip(path_in)
                files.append(sts)
            except:
                continue
        
        elif sts.endswith('gz'):
         
            try:
                wb.unzip_gz(path_in)
                files.append(sts)
            except:
                continue

    return files 
            
def convert_and_remove(path_to_save, files):
    root = path_to_save[:3]
    last = []
    msg = 'converting'
    for fn in tqdm(os.listdir(path_to_save), msg):
        path_in = os.path.join(path_to_save, fn)
        if fn not in files:
            wb.crx2rnx(path_in, root)
     
        if not fn.endswith('o'):
            last.append(path_in)
            
    
    for fn in last:
        os.remove(fn)
        
    return None
         
def filter_stations_by_latitude():
    import pandas as pd
    import GEO as gg 

    sites = gg.load_coords(2022)

    df = pd.DataFrame(sites).T

    df.columns = ['lon', 'lat', 'alt']
    
    return df.loc[df.lat > -15].index


def locate_last_folder(path):
    
    fns = os.listdir(path.rinex)
    
    to_nums = [int(n) for n in fns ]
    
    if len(to_nums) == 0:
        return 1
    else:
        return max(to_nums) 
    
    
def download_rinex_yearly(year, stations, root = 'C:\\'):
    
    path = gs.paths(year, root = root)
    
    b.make_dir(path.rinex_base) # criar o diretório do ano
    
    last_dw = locate_last_folder(path)
    
    for doy in range(last_dw, 366, 1):
         
        path_to_save = f"{path.rinex}{doy:03d}"
        
        b.make_dir(path_to_save) # criar o diretório do doy
        print('Starting RINEX', doy, year)
        download_rinex(
                year, 
                doy,
                path_to_save,
                stations,
                network = 'ibge',         
                )
        
        files = uncompress(path_to_save)
        
        convert_and_remove(path_to_save, files)



