import Webscrape as wb
import GNSS as gs
import base as b



def download_gnss(year, rinex = True):
    
    
    sdoy = b.last_folder_modified(
        gs.paths(year, 0).rinex
        )

            
    for doy in range(1, 366, 1):
        
        path = gs.paths(year, doy)
        
        # if rinex:
        wb.download_rinex(
                path,
                wb.miss_stations(path),
                network = 'ibge'
                )
    # else:
        wb.download_orbit(
            year, 
            doy
            )

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


# download_gnss(2023, rinex = True)

import os
path = gs.paths(2023, 313)

# if rinex:
# wb.download_rinex(
#         path,
#         stations = None,
#         network = 'ibge'
# #         )
# for sts in os.listdir(path.rinex):
#     infile = os.path.join(
#         path.rinex,
#         sts
#         )
#     print(sts)
#     if sts.endswith('d'):
#         wb.crx2rnx(infile)
#     else:
#         os.remove(infile)
