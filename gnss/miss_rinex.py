missing  = [
    'alar',
 'alma',
 'amco',
 'amcr',
 'amte',
 'amtg',
 'amua',
 'aplj',
 'apma',
 'babj',
 'babr',
 'bail',
 'bait',
 'bapa',
 'bavc',
 'ceeu',
 'ceft',
 'cesb',
 'cruz',
 'gour',
 'impz',
 'lcuz',
 'lpiu',
 'lpuc',
 'maba',
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
 'pisr',
 'pitn',
 'riob',
 'rnmo',
 'rnna',
 'rnpf',
 'roji',
 'salu',
 'savo',
 'seaj',
 'ssa1',
 'togu',
 'topl',
 'lhyo',
 'mabb',
 'pove',
 'aps1',
 'bepa',
 'crat',
 'pifl',
 'saga',
 'laya',
 'amha',
 'lpmo',
 'ampt',
 'ljic',
 'brft']

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