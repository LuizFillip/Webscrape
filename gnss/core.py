import Webscrape as wb
from GNSS import paths
from base import make_dir




def download_rinex(
        year, 
        doy, 
        stations = None
        ):
    url = wb.rinex_url(year, doy)
    
    path_to_save = paths(year, doy).rinex     
    path_to_save = make_dir(path_to_save)
    
    if stations is not None:
        receivers_list = wb.filter_rinex(
            url, sel_stations = stations
            )
    else:
        receivers_list = wb.request(url)
        
    out = []
    
    for href in receivers_list:
        
        if '.zip' in href:
            print('[download_rinex]', year, doy, href)
            files = wb.download(url, href, path_to_save)
            out.append(files)
            try:
                wb.unzip_rinex(files, year, path_to_save)
            except:
                continue
            
    wb.crx2rnx(year, doy)
           
    return out




    
    
def folders_orbits(year):
    
    make_dir(paths(year).orbit_base)
    
    for const in ["igl", "igr", 'mgex', 'com']:
        
        path_to_save = paths(year).orbit(const = const)
        
        make_dir(path_to_save)
   
    
def download_orbit(
        year: int, 
        doy: int, 
        const = "com", 
        net = 'igs'
        ):
    
    folders_orbits(year)
    
    fname, url = wb.orbit_url(
        year, doy, 
        network = net, 
        const = const
        )

    path_to_save = paths(
        year, doy).orbit(const = const)
    
    for href in wb.request(url):
        if fname in href:
            print('[download_orbit]', year, doy, href)
            files = wb.download(
                url, href, path_to_save)
            wb.unzip_orbit(files)
            
    return path_to_save
                
            

    


def download_missing_mgex(
        year = 2022, 
        const = 'com'
        ):

    for dn in wb.missing_times(year, const):
    
        url, fname = wb.mgex_fname(dn)
        
        doy = dn.day_of_year
        
        path_to_save = paths(
            year, doy
            ).orbit(const = const)
        
        for href in wb.request(url):
            
            if fname in href:
               
                print('[download_orbit]', dn.date(), href)
                
                files = wb.download(
                    url, href, path_to_save)
                                
                wb.unzip_gz(files)

    return None