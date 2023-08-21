import Webscrape as wb
import GNSS as gs
import pandas as pd
from base import make_dir
import os

def download_gnss(year):
    
    stations = wb.get_stations(gs.paths(year))
    
    wb.folders_orbits(year)
    
    doy_max = wb.minimum_doy(year)
        
    for doy in range(35, 40, 1):
        print(doy_max, year)

        wb.download_rinex(
                year, 
                doy,
                stations = stations
                )

        wb.download_orbit(
            year, 
            doy
            )

    return None


def download_single(year = 2018, doy = 260):
    stations = wb.get_stations(gs.paths(year))
    wb.download_rinex(
            year, 
            doy,
            stations = stations
            )
    
def download_orbits(
        year = 2022, 
        const = 'com'
        ):
    
    for doy in range(309, 366, 1):
        
        wb.download_orbit(
                year, 
                doy, 
                const = 'com', 
                net = 'igs'
                )
    
class EMBRACE(object):
    
    def __init__(self, site = 'sao_luis'):
        
        self.save_in = 'D:\\drift\\SAA\\'
        self.site = site
        
    def download_drift(
            self, 
            dn, 
            path_save,
            ext = ['DVL']
            ):

        url = wb.embrace_url(
            dn, 
            site = self.site, 
            inst = 'ionosonde'
            )    
        
        for link in wb.request(url):

            if any(f in link for f in ext):
                wb.download(
                    url, 
                    link, 
                    path_save
                    )
    
    @staticmethod
    def dates(start = 2012, end = 2022):
        s = f'{start}-01-01'
        e = f'{end}-12-31'
        return pd.date_range(s, e, freq = '1D')
    
    
    def download_all(self):
        
        for dn in self.dates():
            doy_path = dn.strftime('%Y/%j//')
            path_save = os.path.join(self.save_in, doy_path)
            make_dir(path_save)
            print('[download_embrace]', dn.date())
            self.download_drift(dn, path_save)


    
# EMBRACE().download_all()


        
        
# download_orbits(2022)
