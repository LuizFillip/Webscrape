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
 'brft', 
 'utar', 'ptre', 'iacr', 
             'pccl', 'cmrc', 'suri', 
             'chyt', 'mnmi', 'psga', 
             'fbaq', 'atjn', 'cgtc', 
             'hmbs', 'picc', 'uape']

import GNSS as gs
import os
import shutil


def miss_stations(path):
        
    in_rinex = os.listdir(path.rinex)
    in_rinex = [rx[:4] for rx in in_rinex]
    
    
    stations = []
    for sts in missing:
        
        if sts not in in_rinex:
            stations.append(sts)
            
    return stations
        
PATH_OUT = 'D:\\database\\GNSS\\tec\\2021\\t001\\'

path = gs.paths(2021, 1)

def move_away(path):

    in_tec = os.listdir(path.tec)
    in_tec = [rx[:4] for rx in in_tec]
    
    for sts in in_tec:
        
        if sts not in missing:
            
            dst = os.path.join(
                PATH_OUT,
                f'{sts}.txt'
                )
            
            src = path.fn_tec(sts)
            
            shutil.move(src, dst)