import sys
import gnss as gnss 
import os
os.path.dirname(sys.executable)
from pathlib import Path



class paths(object):
    """Construct file paths from input date (year and doy)"""

    def __init__(self, 
                 year: int = 2014, 
                 doy: int = 1, 
                 root = str(Path.cwd())):
        
        if doy == 0:
            self.doy = ""
        else:
            
            self.date =  gnss.date_from_doy(year, doy)
            self.week, self.number = gnss.gpsweek_from_date(self.date)
            self.doy = self.date.strftime("%j")
            
            
        self.root = root
        if "data-analysis" in self.root:
            self.current_path = os.path.join(
                self.root, 
                "database", 
                "GNSS")
        else:
            self.current_path = os.path.join(
                self.root, 
                "database") 
        
        self.year = str(year)
        
        self.ext_rinex = self.year[-2:] + "o"
        
    
    def orbit(self, const = "igr"):
        return os.path.join(
            self.current_path, "orbit", 
            self.year, const)
    @property
    def rinex(self):
        return os.path.join(
            self.current_path, "rinex", 
            self.year, self.doy)
    @property
    def tec(self):
        return os.path.join(
            self.current_path, "tec", 
            self.year, self.doy)
    @property
    def roti(self):
        return os.path.join(
            self.current_path, "roti", 
                            self.year)
    @property
    def dcb(self):
        return os.path.join(
            self.current_path, "dcb", 
                            self.year)
    @property
    def json_gen(self):
        return os.path.join(
            self.current_path, "json")
    
    @property
    def json(self):
        return os.path.join(
            self.current_path, "json", self.year)
    @property
    def prns(self):
        fname = f"{self.doy}.txt"
        return os.path.join(
            self.current_path, "prns", 
                            self.year, fname)
    @property
    def fn_json(self):
        fname = f"{self.doy}.json"
        return os.path.join(
            self.json, fname)
    
    @property
    def fn_json_gen(self):
        return f"{self.json}.json"
    
    @property
    def fn_roti(self):
        fname = f"{self.doy}.txt"
        return os.path.join(self.roti, fname)
    
    def fn_orbit(self, const = "igr"):
        fname = f"{const}{self.week}{self.number}.sp3"
        return os.path.join(self.orbit(const), fname)
    
    def fn_tec(self, station = "alar"):
        fname =  f"{station}.txt"
        return  os.path.join(self.tec, fname)
    
    def fn_rinex(self, station = "alar"):
        fname = f"{station}{self.doy}1.{self.ext_rinex}"
        return os.path.join(self.rinex, fname)
    
    def fn_dcb(self, mgx = True):
        if mgx:
            fname = f"CAS0MGXRAP_{self.year}{self.doy}0000_01D_01D_DCB.BSX" 
            return os.path.join(self.dcb, fname)
    
    
class prns:
    """Creating a prn list for each constellation"""
    
    def __init__(self):
        pass
    @staticmethod
    def format_prn(constelation, num):
        if num < 10:
            prn = f"{constelation}0{num}"
        else:
            prn = f"{constelation}{num}"
        return prn
    
    @staticmethod
    def prn_list(constelation = "G", number = 32):
        call = prns()
        return [call.format_prn(constelation, num) 
                for num in range(1, number + 1)]
    
    @property
    def gps_and_glonass(self):
        call = prns()
        return call.prn_list("G", 32) + call.prn_list("R", 24)
        





        
