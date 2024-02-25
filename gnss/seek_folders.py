import os 
import GNSS as gs 


def date_from_fname(fname):
    week = int(fname[3:7])
    number = int(fname[7:8])

    return gs.doy_from_gpsweek(week, number)



class minimum_doy(object):
    
    def __init__(self, path):
        
        self.path = path
        
    def orbit(self, const = 'com'):
        
        path = self.path.orbit(const)
        
        return max([date_from_fname(f)[1] for f 
             in os.listdir(path)])

    @property
    def rinex(self):
        return self.cond_max(
            self.list_doy(self.path.rinex)
            )
    
    @property   
    def tec(self):
        return self.cond_max(
            self.list_doy(self.path.tec)
            )
    
    @property   
    def roti(self):
        list_doy = [
            int(f.replace('.txt', '')) 
            for f in os.listdir(self.path.roti)
            ]
        return self.cond_max(list_doy)
    
    @staticmethod
    def list_doy(path):
        return [int(f) for f in 
                os.listdir(path) if f != '365']
    
    @staticmethod
    def cond_max(list_doy):
        if len(list_doy) == 0:
            return 1
        else:
            return max(list_doy)
        
