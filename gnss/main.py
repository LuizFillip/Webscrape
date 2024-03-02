import Webscrape as wb
import GNSS as gs

ibge_stations= ['amco', 'amcr', 'amha', 'ampt', 'amte', 'amua', 'aplj', 'apma', 'aps1', 
           'bele', 'bepa', 'impz', 'maba', 'mabb', 'mtji', 'naus', 'paar', 'pait',
           'pasm', 'pove', 'riob', 'rogm', 'roji', 'salu', 'cruz', 'rogu', 'rovi', 
           'ceeu', 'ceft', 'rnna', 'pbjp']


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

for year in range(2013, 2022):
    download_gnss(year, igs_stations)
