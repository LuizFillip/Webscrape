missing = ['alar',
 'alma',
 'amco',
 'amcr',
 'amha',
 'ampt',
 'amte',
 'amtg',
 'amua',
 'aplj',
 'apma',
 'aps1',
 'bapa',
 'bepa',
 'brft',
 'ceeu',
 'ceft',
 'cesb',
 'crat',
 'cruz',
 'maba',
 'mabb',
 'mabs',
 'mtji',
 'naus',
 'paar',
 'pait',
 'pasm',
 'pbcg',
 'pbjp',
 'pbpt',
 'peaf',
 'pepe',
 'perc',
 'picr',
 'pifl',
 'pisr',
 'pitn',
 'pove',
 'riob',
 'rnmo',
 'rnna',
 'rnpf',
 'roji',
 'saga',
 'salu',
 'seaj',
 'togu',
 'topl']

import Webscrape as wb
import GNSS as gs
import os

# path = gs.paths(2021, 2)

def miss_stations(path):
        
    in_rinex = os.listdir(path.rinex)
    in_rinex = [rx[:4] for rx in in_rinex]
    
    
    stations = []
    for sts in missing:
        
        if sts not in in_rinex:
            stations.append(sts)
            
    return stations
        
        
# wb.download_rinex(
#         path, 
#         stations 
#         )