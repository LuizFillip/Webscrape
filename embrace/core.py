import datetime as dt
import Webscrape as wb

PATH_IONO = 'database/iono/'

def download_multiple_iono(start):
    
    for site in ['fortaleza', 'boa_vista', 'sao_luis']:
        wb.download_from_periods(start, site)
    


    
class EMBRACE(object):
    
    def __init__(
            self, 
            site = 'sao_luis', 
            save_in = 'D:\\drift\\SAA\\'
            ):
        
        self.save_in = save_in 
        self.site = site
        
    def download_drift(
            self, 
            dn, 
            ext = ['DVL']
            ):

        url = wb.embrace_url(
            dn, 
            site = self.site, 
            inst = 'ionosonde'
            )    
        
        for link in wb.request(url):
            
            if any(f in link for f in ext):
                
                delta = dt.timedelta(hours = 4)
                
                if ((wb.iono_dt(link) >= dn)and 
                    (wb.iono_dt(link) <= dn + delta)):
                   
                    print('[download_iono]', link)
                    wb.download(
                        url, 
                        link, 
                        self.save_in
                        )
                
    

        