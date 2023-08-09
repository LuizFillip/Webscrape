import gnsscal
import datetime as dt
import Webscrape as wb 
import os


infos = {
    "ibge" : 'https://geoftp.ibge.gov.br/informacoes_sobre_posicionamento_geodesico/rbmc/dados', 
    "igs": 'https://igs.bkg.bund.de/root_ftp/IGS/products/', 
    "igs2": 'https://files.igs.org/pub/'
    }

regions = {"stations_1": 
               ['alar',
                 'bair',
                 'brft',
                 'ceeu',
                 'ceft',
                 'cesb',
                 'crat',
                 'pbcg',
                 'pbjp',
                 'peaf',
                 'pepe',
                 'recf',
                 'rnmo',
                 'rnna',
                 'seaj'], 
           
           'stations_2': 
               ['apsa',
                'cruz',
                'impz',
                'maba',
                'mabb',
                'mapa',
                'paat',
                'pait',
                'past',
                'pove',
                'riob',
                'rogm',
                'salu']
           
           }

    

def make_dir(path: str):
    """
    Create a new directory by 
    path must be there year and doy
    """
    try:
        os.mkdir(path)
    except OSError:
        print(f"Creation of the directory {path} failed")
    
    return path


def date_from_doy(year: int, doy:int) -> dt.date:
    """Return date from year and doy"""
    return dt.date(year, 1, 1) + dt.timedelta(doy - 1)

def gpsweek_from_date(date: dt.date) -> tuple:
    """Return GPS week and number from date"""
    return gnsscal.date2gpswd(date)


def gpsweek_from_doy_and_year(year: int, doy:int) -> tuple:
    """Return GPS week and number from date"""
    return gnsscal.date2gpswd(date_from_doy(year, doy))


def rinex_url(year:int, doy:int, network:str = "ibge"):
    date = date_from_doy(year, doy)
    doy_str = date.strftime("%j")
    return f"{infos[network]}/{year}/{doy_str}/"


def orbit_url(
        year:int, 
        doy:int, 
        network:str = "IGS", 
        const:str = "igr"
        ):
    
    """Build urls and filenames from year, doy and GNSS system"""
    
    week, number = gpsweek_from_doy_and_year(year, doy)
    
    url = infos[network]

    if network == "igs":

        if const == "igr":
            url += f"orbits/{week}/"
            filename = f"{const}{week}{number}.sp3.Z"

        elif const == "igl":
            url += f"glo_orbits/{week}/"
            filename = f"{const}{week}{number}.sp3.Z"
            
    elif network == "igs2":
        
        if const == "igr":
            url += f"orbits/{week}/"
            filename = f"{const}{week}{number}.sp3.Z"

        
        elif const == "igl":
            url += f"glonass/products/{week}/"
            filename = f"{const}{week}{number}.sp3.Z"
        
        
    return filename, url


def filter_rinex(
        url:str, 
        sel_stations: list = regions["stations_2"]
        ):
  out = []
  for href in wb.request(url):
      
      rules = [f in href for f in sel_stations]
      if any(rules):
          out.append(href)
          
  return out

import GNSS as gs


def minimum_doy(year, root = 'D:\\'):
    path = gs.paths(year, doy = 0, root = root).rinex
    list_doy = [int(f) for f in os.listdir(path) if f != '365']
    return max(list_doy)



