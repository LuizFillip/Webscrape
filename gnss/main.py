import Webscrape as wb
import GNSS as gs
import base as b 

ibge_stations= ['amco', 'amcr', 'amha', 'ampt', 'amte',
                'amua', 'aplj', 'apma', 'aps1', 'bele', 
                'bepa', 'impz', 'maba', 'mabb', 'mtji', 
                'naus', 'paar', 'pait', 'pasm', 'pove', 
                'riob', 'rogm', 'roji', 'salu', 'cruz', 
                'rogu', 'rovi', 'ceeu', 'ceft', 'rnna', 'pbjp']


# igs_stations = ['areg', 'riop',  'antf', 'iqqe', 'qui3']

def download_gnss(year, stations, network = 'ibge', root = 'C:\\'):
    
    for doy in range(2, 366, 1):
        
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
# 
# for year in [2012,2024,2025]:
    
#     download_gnss(year, ibge_stations)


