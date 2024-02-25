import Webscrape as wb
import GNSS as gs
import base as b

stations= ['amco', 'amcr', 'amha', 'ampt', 'amte', 'amua', 'aplj', 'apma', 'aps1', 'bele', 'bepa', 'impz', 'maba', 'mabb', 'mtji', 'naus', 'paar', 'pait', 'pasm', 'pove', 'riob', 'rogm', 'roji', 'salu', 'cruz', 'rogu', 'rovi', 'ceeu', 'ceft', 'rnna', 'pbjp']

stations = ['AREG', 'areg', 'ANTF', 'IQQ', 'QUI']

def download_gnss(year, stations, network = 'igs'):
    
    for doy in range(1, 365, 1):
        
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

year = 2019
download_gnss(year, stations, network = 'igs')


