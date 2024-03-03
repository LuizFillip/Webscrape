import Webscrape as wb
import GNSS as gs



igs_stations = ['areg', 'riop',  'antf', 'iqqe', 'qui3']

def download_gnss(year, stations, network = 'garner'):
    
    for doy in range(1, 366, 1):
        
        path = gs.paths(year, doy)
        
        # if rinex:
        wb.download_rinex(
                path,
                stations,
                network
                )
        # else:
        # wb.download_orbit(
        #     year, 
        #     doy
        #     )

    return None


def chile(year = 2021):

    stations = ['utar', 'ptre', 'iacr', 
                'pccl', 'cmrc', 'suri', 
                'chyt', 'mnmi', 'psga', 
                'fbaq', 'atjn', 'cgtc', 
                'hmbs', 'picc', 'uape']
    

    for doy in range(1, 366, 1):
        path = gs.paths(year, doy)
    
        wb.download_rinex(
                path, 
                stations, 
                network = 'chile' 
                )

for year in range(2016, 2022):
    download_gnss(year, igs_stations)
