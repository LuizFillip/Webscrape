import Webscrape as wb
import GNSS as gs
import base as b
import shutil

def folders_orbits(year):
    
    b.make_dir(gs.paths(year).orbit_base)
    
    for const in ["igl", "igr", 'igv', 'cod',
                  'igs', 'mgex', 'com']:
        
        path_to_save = gs.paths(year).orbit(const = const)
        
        b.make_dir(path_to_save)
        
        
infos = {
    "igs": 'https://igs.bkg.bund.de/root_ftp/IGS/products/', 
    "igs2": 'https://files.igs.org/pub/', 
    'garner': 'http://garner.ucsd.edu/pub/products/',
    
    }

def orbit_url(
        year:int, 
        doy:int, 
        network:str = "igs", 
        const:str = "igr"
        ):
    
    """
    Build urls and filenames from year, doy and GNSS        
    system
    """
    
    week, number = gs.gpsweek_from_doy_and_year(
        year, doy)
    
    date = gs.date_from_doy(year, doy)
    strd = date.strftime('%j')
    url = infos[network]

    if network == "igs":

        if const == "igr":
            url += f"orbits/{week}/"
            filename = f"{const}{week}{number}.sp3.Z"

        elif const == "igl":
            url += f"glo_orbits/{week}/"
            filename = f"{const}{week}{number}.sp3.Z"
            
        elif const == 'com':
            url += f"mgex/{week}/"
            filename = f'{const}{week}{number}.eph.Z'
            
        elif const == 'cod':
            
            url += f"orbits/{week}/"
            filename = f'cod{week}{number}.eph.Z'
            
        elif const == 'igv':
            url += f"orbits/{week}/"
            filename = f'igv{week}{number}_00.sp3.Z'
            
        elif const == 'igs':
            url += f"orbits/{week}/"
            filename = f'igs{week}{number}.sp3.Z'
            
        elif const == 'mgex':
            filename = f'IGS0OPSULT_{year}{strd}1800_02D_15M_ORB.SP3.gz'
            url += f"{week}/"
    
    elif network == 'garner':
        if const == "igv":
            filename = f'igv{week}{number}_00.sp3.Z'
            url += f"{week}/"
           
         
    elif network == "igs2":
        
        if const == "igr":
            url += f"orbits/{week}/"
            filename = f"{const}{week}{number}.sp3.Z"

        
        elif const == "igl":
            url += f"glonass/products/{week}/"
            filename = f"{const}{week}{number}.sp3.Z"
            
        elif const == 'igv':
            url += f"glonass/products/{week}/"
            filename = 'com{week}{number}.eph.Z'
        

    return filename, url



        

                


def download_single(year = 2018, doy = 260):
    stations = wb.get_stations(gs.paths(year))
    wb.download_rinex(
            year, 
            doy,
            stations = stations
            )

        
def copy_rewrite(src):
    
    dst = src.replace('igv', 'cod').replace('_00', '')
    shutil.copy(src, dst)

def download_orbit(
        year: int, 
        doy: int, 
        const = "igv", 
        network = 'garner'
        ):

    fname, url = orbit_url(
        year, doy, 
        network = network, 
        const = const
        )
            
    
    path_to_save = gs.paths(
        year, doy).orbit(const = const)
    
    
    for href in wb.request(url):
        if fname in href:        
            print('[download_orbit]', year, doy, href)
            path_in = wb.download(
                url, href, path_to_save
                )
            src = wb.unzip_Z(path_in)
            
            copy_rewrite(src)
            
    
def download_orbits(
        year = 2022, 
        const = 'igv', 
        network = 'garner'
        ):
    
    for doy in range(1, 366, 1):
        download_orbit(
                year, 
                doy, 
                const, 
                network 
                )
year = 2023 
doy= 1

const = 'igv'

download_orbits(
        year = 2023
        )
        
