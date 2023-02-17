import gnsscal
import datetime as dt
from core import request

infos = {"ibge" : 'https://geoftp.ibge.gov.br/informacoes_sobre_posicionamento_geodesico/rbmc/dados', 
         "igs": 'https://igs.bkg.bund.de/root_ftp/IGS/products/', 
         "igs2": 'https://files.igs.org/pub/'}

regions = {"sts1": ['alar', 'bair', 'brft', 'ceeu', 
                       'ceft', 'cesb', 'crat', 'pbcg', 
                       'pbjp', 'peaf', 'pepe', 'recf',
                       'rnmo', 'rnna', 'seaj']}


def date_from_doy(year: int, doy:int) -> dt.date:
    """Return date from year and doy"""
    return dt.date(year, 1, 1) + dt.timedelta(doy - 1)

def gpsweek_from_doy_and_year(year: int, doy:int) -> tuple:
    """Return GPS week and number from date"""
    return gnsscal.date2gpswd(date_from_doy(year, doy))


def rinex_url(year:int, doy:int, network:str = "IBGE"):
    date = date_from_doy(year, doy)
    doy_str = date.strftime("%j")
    return f"{infos[network]}/{year}/{doy_str}/"


def orbit_url(year:int, 
              doy:int, 
              network:str = "IGS", 
              const:str = "igr"):
    
    
    
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


def filter_rinex(url:str, 
                 sel_stations: list = regions["sts1"]
                 ):
  out = []
  for href in request(url):
      
      rules = [f in href for f in sel_stations]
      if any(rules):
          out.append(href)
          
  return out

filename, url = orbit_url(2013, 1, network = "igs2", const = "igl")

url = "https://files.igs.org/pub/glonass/products/1721/"
print(request(url))