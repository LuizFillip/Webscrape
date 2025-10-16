import Webscrape as wb
import GNSS as gs
import base as b 



def download_gnss(year, stations, network = 'ibge', root = 'C:\\'):
    
    for doy in range(207, 366, 1):
        
        path = gs.paths(year, doy, root = root)
        
        b.make_dir(path.rinex_base)
        
        wb.download_rinex(
                path,
                stations,
                network
                )
        # # else:
        # wb.download_orbit(
        #     year, 
        #     doy
        #     )

    return None


def chile(year = 2021):

    stations = [
        'utar', 'ptre', 'iacr', 
        'pccl', 'cmrc', 'suri', 
        'chyt', 'mnmi', 'psga', 
        'fbaq', 'atjn', 'cgtc', 
        'hmbs', 'picc', 'uape'
        ]
    

    for doy in range(1, 366, 1):
        path = gs.paths(year, doy)
    
        wb.download_rinex(
                path, 
                stations, 
                network = 'chile' 
                )
# 
# for year in [2012,2024,2025]:
    
#     download_gnss(year, ibge_stations)


# year = 2012
# root = 'C:\\'

# stations = wb.filter_stations_by_latitude()

# wb.download_rinex_yearly(year, stations, root)