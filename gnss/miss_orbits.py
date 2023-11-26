import Webscrape as wb 
import GNSS as gs

def download_missing_mgex(
        year = 2022, 
        const = 'com'
        ):
    
    wb.folders_orbits(year)

    for dn in wb.missing_times(year, 'com'):
    
        url, fname = wb.mgex_fname(dn)
        
        doy = dn.timetuple().tm_yday
        
        path_to_save = gs.paths(
            year, doy
            ).orbit(const = 'cod')
        
        for href in wb.request(url):
            
            if fname in href:
               
                print('[download_orbit]', dn, href)
                
                files = wb.download(
                    url, href, path_to_save)
                                
                wb.unzip_gz(files)

    return None


def download_missing_other_const(
        in_const = 'com',
        out_const = 'cod',
        year = 2020
        ):
    
    
    for dn in wb.missing_times(year, in_const):
        doy = dn.timetuple().tm_yday
        wb.download_orbit(
                year, 
                doy, 
                const = out_const, 
                net = 'igs'
                )

    wb.copy2com(
        out_const, 
        in_const, 
        year = 2020)
    