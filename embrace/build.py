import embrace as ec
import os 

class directories(object):
    
    """
    Create directories from input names:
        inst: intrumentation type (e.g. imager)
        site: site location for each inst.
        year: observation year
        root: path root
    """
    
    def __init__(
            self, inst, site, year, root,
             ):
  
        self.root = str(root)
        self.year = str(year)
        self.name_dir = ec.site_codes[inst][site][:3]
        
    @staticmethod
    def create_dir(path):
        try:
            os.mkdir(path)
        except OSError:
            print(f"{path} wasn`t created")         
        return path
        
    @property  
    def site_path(self):
        return self.create_dir(
                    os.path.join(
                    self.root, 
                    self.name_dir))
        
    @property
    def year_path(self): 
        return self.create_dir(
                    os.path.join(
                    self.root, 
                    self.name_dir, 
                    self.year))
    
    def doy_path(self, doy): 
        return self.create_dir(
                    os.path.join(
                    self.root, 
                    self.name_dir, 
                    self.year, 
                    str(doy)))