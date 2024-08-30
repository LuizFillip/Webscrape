import Webscrape as wb
import GNSS as gs
from base import make_dir
import os

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



def filter_by_stations(href, stations):
    if any([z in href for z in stations]):
        ends = ['d.zip', 'd.Z', 'crx.gz']
        if any([href.endswith(e) for e in ends]):
           return True
        else:
           return False
    else:
        return False
    

def filter_rinex(
        url: str, 
        sel_stations: list[str]
        ):
    
  out = []
  for href in wb.request(url):
      
      rules = [f in href for f in sel_stations]
      if any(rules):
          out.append(href)
          
  return out




def download_rinex(
        path,
        stations = None,
        network = 'ibge'
        ):
    
    year, doy = int(path.year), int(path.doy)
    
    url = rinex_url(year, doy, network)

    path_to_save = path.rinex
    make_dir(path_to_save)
    print('[starting]', path.doy)
    for href in wb.request(url):

        # if filter_by_stations(href, stations):
        ends = ['.zip', 'd.Z', 'crx.gz']
        if any([href.endswith(e) for e in ends]):
           print('[download_rinex]', href)
           wb.download(
               url, 
               href, 
               path_to_save
               )
           
        
    uncompress_convert(path.rinex)

    return None



def uncompress_convert(path_root):
    unzip_msg = '[unzip_rinex]'
    for sts in os.listdir(path_root):
        path_in = os.path.join(path_root, sts)
        
        if sts.endswith('Z'):
            print(unzip_msg, sts)
            try:
                wb.unzip_Z(path_in)
            except:
                continue
            
        elif sts.endswith('zip'):
            print(unzip_msg, sts)
            try:
                wb.unzip_zip(path_in)
            except:
                continue
        
        elif sts.endswith('gz'):
            print(unzip_msg, sts)
            try:
                wb.unzip_gz(path_in)
            except:
                continue
            
    for sts in os.listdir(path_root):
        path_in = os.path.join(path_root, sts)
        if sts.endswith('d') or sts.endswith('crx'):
            print('[convert_rinex]', sts)
            wb.crx2rnx(path_in)
            
    return None
            

        
def test_one_day_download(year, doy, network = 'garner'):
        
    stations = ['areg', 'riop',  'antf', 'iqqe', 'qui3']
    path = gs.paths(year, doy, root = 'D:\\')
        
    download_rinex(
                path,
                stations = stations,
                network = network
                )

def test_filter_stations(year, doy):

    url = wb.rinex_url(year, doy, network = 'garner')
    
    stations = ['areg', 'riop',  'antf', 'iqqe', 'qui3']
    
    for href in wb.request(url):
        if filter_by_stations(href, stations):
            print(href)
            
