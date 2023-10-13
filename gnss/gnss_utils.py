import Webscrape as wb 
import os
import GNSS as gs
from base import make_dir 

def folders_orbits(year):
    
    make_dir(gs.paths(year).orbit_base)
    
    for const in ["igl", "igr", 'igv', 'cod',
                  'igs', 'mgex', 'com']:
        
        path_to_save = gs.paths(year).orbit(const = const)
        
        make_dir(path_to_save)
   

infos = {
    "ibge" : 'https://geoftp.ibge.gov.br/informacoes_sobre_posicionamento_geodesico/rbmc/dados', 
    "igs": 'https://igs.bkg.bund.de/root_ftp/IGS/products/', 
    "igs2": 'https://files.igs.org/pub/', 
    'chile': 'http://gps.csn.uchile.cl/data/', 
    'lisn': 'http://lisn.igp.gob.pe/jdata/database/gps/rinex/',
    'gage': 'https://gage-data.earthscope.org/archive/gnss/rinex/obs/2013/001'
    }



def rinex_url(
        year:int, 
        doy:int, 
        network:str = "ibge"
        ):
    date = gs.date_from_doy(year, doy)
    doy_str = date.strftime("%j")
    return f"{infos[network]}/{year}/{doy_str}/"


def orbit_url(
        year:int, 
        doy:int, 
        network:str = "igs", 
        const:str = "igr"
        ):
    
    """
    Build urls and filenames from year, doy and GNSS        
    system
    """
    
    week, number = gs.gpsweek_from_doy_and_year(
        year, doy)
    
    url = infos[network]

    if network == "igs":

        if const == "igr":
            url += f"orbits/{week}/"
            filename = f"{const}{week}{number}.sp3.Z"

        elif const == "igl":
            url += f"glo_orbits/{week}/"
            filename = f"{const}{week}{number}.sp3.Z"
            
        elif const == 'com':
            url += f"mgex/{week}/"
            filename = f'{const}{week}{number}.eph.Z'
            
        elif const == 'cod':
            
            url += f"orbits/{week}/"
            filename = f'cod{week}{number}.eph.Z'
            
        elif const == 'igv':
            url += f"orbits/{week}/"
            filename = f'igv{week}{number}_00.sp3.Z'
            
        elif const == 'igs':
            url += f"orbits/{week}/"
            filename = f'igs{week}{number}.sp3.Z'
       
         
    elif network == "igs2":
        
        if const == "igr":
            url += f"orbits/{week}/"
            filename = f"{const}{week}{number}.sp3.Z"

        
        elif const == "igl":
            url += f"glonass/products/{week}/"
            filename = f"{const}{week}{number}.sp3.Z"
            
        elif const == 'igv':
            url += f"glonass/products/{week}/"
            filename = 'com{week}{number}.eph.Z'
        
        
    return filename, url


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

def mgex_fname(dn):
    doy = dn.strftime('%j')
    year = dn.year
    doy = dn.timetuple().tm_yday
    week, number = gs.gpsweek_from_doy_and_year(
        year, doy)
    
    url = infos['igs'] + f'{week}/'
    
    return url, f'IGS0OPSFIN_{year}{doy}0000_01D_15M_ORB.SP3.gz'




def date_from_fname(fname):
    week = int(fname[3:7])
    number = int(fname[7:8])

    return gs.doy_from_gpsweek(week, number)



class minimum_doy(object):
    
    def __init__(self, path):
        
        self.path = path
        
    def orbit(self, const = 'com'):
        
        path = self.path.orbit(const)
        
        return max([date_from_fname(f)[1] for f 
             in os.listdir(path)])

    @property
    def rinex(self):
        return self.cond_max(
            self.list_doy(self.path.rinex)
            )
    
    @property   
    def tec(self):
        return self.cond_max(
            self.list_doy(self.path.tec)
            )
    
    @property   
    def roti(self):
        list_doy = [
            int(f.replace('.txt', '')) 
            for f in os.listdir(self.path.roti)
            ]
        return self.cond_max(list_doy)
    
    @staticmethod
    def list_doy(path):
        return [int(f) for f in 
                os.listdir(path) if f != '365']
    
    @staticmethod
    def cond_max(list_doy):
        if len(list_doy) == 0:
            return 1
        else:
            return max(list_doy)
        



