import Webscrape as wb 
import GNSS as gs

def copy_rename_files(year = 2023, doy = 1):
    const_in = 'igv'
    const_out = 'com'

    path_in = gs.paths(year, doy).orbit(const = const_in) 
    path_out = gs.paths(year, doy).orbit(const = const_out) 
    
    for src in os.listdir(path_in):
        dst = src.replace(
            'igv', 'com'
            ).replace('_00', '').replace('sp3', 'EPH')
        shutil.copy(
            os.path.join(path_in, src), 
            os.path.join(path_out, dst)
            )

    return None 
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
    