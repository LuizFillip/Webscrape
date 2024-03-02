import Webscrape as wb 
import GNSS as gs


networks = {
    "ibge" : 'https://geoftp.ibge.gov.br/informacoes_sobre_posicionamento_geodesico/rbmc/dados', 
    'igs': 'https://igs.bkg.bund.de/root_ftp/IGS/obs/',
    'chile': 'http://gps.csn.uchile.cl/data/', 
    'lisn': 'http://lisn.igp.gob.pe/jdata/database/gps/rinex/',
    'gage': 'https://gage-data.earthscope.org/archive/gnss/rinex/obs/',
    'garner': 'http://garner.ucsd.edu/pub/rinex/'
    }

'https://igs.bkg.bund.de/root_ftp/IGS/obs/2019/086/'

def rinex_url(year, doy, network = "ibge"):
    date = gs.date_from_doy(year, doy)
    doy_str = date.strftime("%j")
    return f"{networks[network]}/{year}/{doy_str}/"




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

def rinex3_fname(dn):
    doy = dn.strftime('%j')
    year = dn.year
    doy = dn.timetuple().tm_yday
    week, number = gs.gpsweek_from_doy_and_year(year, doy)
    
    url = networks['igs'] + f'{week}/'
    
    return url, f'IGS0OPSFIN_{year}{doy}0000_01D_15M_ORB.SP3.gz'



