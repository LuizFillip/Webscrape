# import Webscrape as wb
# import GNSS as gs
# import base as b
# import shutil
# import pandas as pd 
# import os 
# import datetime as dt 

# infos = {
#     "igs": 'https://igs.bkg.bund.de/root_ftp/IGS/products/', 
#     "igs2": 'https://files.igs.org/pub/', 
#     'garner': 'http://garner.ucsd.edu/pub/products/',
    
#     }

# consts = ["igl", "igr"]# 'igv', 'cod', 'igs', 'mgex', 'com']

# def folders_orbits(year):
    
#     b.make_dir(gs.paths(year).orbit_base)
    
#     for const in consts:
        
#         path_to_save = gs.paths(year).orbit(const = const)
        
#         b.make_dir(path_to_save)
        
#     return None 

# def orbit_url(
#         dn, 
#         network:str = "igs", 
#         const:str = "igr"
#         ):
    
#     """
#     Build urls and filenames from year, doy and GNSS        
#     system
#     """
    
#     week, number = gs.dn2gpsweek(dn)

#     strd = dn.strftime('%j')
#     url = infos[network]

#     if network == "igs":

#         if const == "igr":
#             url += f"orbits/{week}/"
#             filename = f"{const}{week}{number}.sp3.Z"

#         elif const == "igl":
#             url += f"glo_orbits/{week}/"
#             filename = f"{const}{week}{number}.sp3.Z"
            
#         elif const == 'com':
#             url += f"mgex/{week}/"
#             filename = f'{const}{week}{number}.eph.Z'
            
#         elif const == 'cod':
            
#             url += f"orbits/{week}/"
#             filename = f'cod{week}{number}.eph.Z'
            
#         elif const == 'igv':
#             url += f"orbits/{week}/"
#             filename = f'igv{week}{number}_00.sp3.Z'
            
#         elif const == 'igs':
#             url += f"orbits/{week}/"
#             filename = f'igs{week}{number}.sp3.Z'
            
#         elif const == 'mgex':
#             year = dn.year
#             filename = f'IGS0OPSULT_{year}{strd}1800_02D_15M_ORB.SP3.gz'
#             url += f"{week}/"
    
#     elif network == 'garner':
        
#         if const == "igv":
#             filename = f'igv{week}{number}_00.sp3.Z'
#             url += f"{week}/"
            
#         elif const == 'esa':
#             filename = f'esa{week}{number}.sp3.Z'
#             url += f"{week}/"
         
#     elif network == "igs2":
        
#         if const == "igr":
#             url += f"orbits/{week}/"
#             filename = f"{const}{week}{number}.sp3.Z"

        
#         elif const == "igl":
#             url += f"glonass/products/{week}/"
#             filename = f"{const}{week}{number}.sp3.Z"
            
#         elif const == 'igv':
#             url += f"glonass/products/{week}/"
#             filename = 'com{week}{number}.eph.Z'
        

#     return filename, url


# def download_single(year = 2018, doy = 260):
#     stations = wb.get_stations(gs.paths(year))
#     wb.download_rinex(
#             year, 
#             doy,
#             stations = stations
#             )
    
#     return None 


# def fn2dn(fn):
#     gpsweek, dayofweek = int(fn[3:7]), int(fn[7:8])  
#     return gs.gpsweek2dn(gpsweek, dayofweek)

# def copy_rewrite(src):
    
#     dst = src.replace('igv', 'cod').replace('_00', '')
#     shutil.copy(src, dst)
    
#     return None 

# def download_orbit(
#         dn, 
#         const = "igv", 
#         network = 'garner', 
#         root = 'C:\\'
#         ):

#     fname, url = orbit_url(
#         dn, 
#         network = network, 
#         const = const
#         )
            
   
      
   
            
        
    
#     return None 
    

# def last_download(year, const, root = 'E:\\'):
        
#     path = gs.paths(year, doy = 0, root = root)
    
#     pin = path.orbit(const = const) 
    
#     b.make_dir(path.orbit_base)
    
#     path_to_save = path.orbit(const = const)
    
#     b.make_dir(path_to_save)
    
#     files = [fn2dn(fn) for fn in os.listdir(pin)]
    
#     if len(files) == 0:
#         return dt.datetime(year, 1, 1)
#     else:
#         return max(files) 
    
# def igv_sp3_name(fn):
#     return fn.replace('_00', '').replace('.Z', '')

# def rename_igv(year, root = 'E:\\'):
    
#     path_in = gs.paths(year, root = root).orbit(const = 'igv')
    
#     for fn in os.listdir(path_in):
#         src = os.path.join(path_in, fn)
#         dst = os.path.join(path_in, fn.replace('_00', ''))
#         os.rename(src, dst)
        
#     return None
        
# def download_orbits_dialy(
#         year = 2022, 
#         root = 'E:\\', 
#         const = 'esa',
#         network = 'garner'
#         ):
    
#     sts, end = f'{year}-01-01', f'{year}-12-31'
      
#     # sts = last_download(year, const, root = root)
    
#     # print(sts)
#     # print('Starting downloading', year)
#     for dn in pd.date_range(sts, end):
        
#         path = gs.paths(dn, root = root)
        
#         fn, url = orbit_url(
#             dn, 
#             network = network, 
#             const = const
#             )
        
#         path_in = os.path.join(
#             path.orbit(const = const), 
#             igv_sp3_name(fn)
#             )
        
#         b.make_dir(path.orbit_base)
        
#         path_to_save = path.orbit(const = const)
        
#         b.make_dir(path_to_save)
        
#         if os.path.exists(path_in):
#             continue
#         else:
            
                 
#             for href in wb.request(url):
#                 if fn in href:        
#                     print('[download_orbit]', dn.date(), href)
                     
#                     path_in = wb.download(
#                         url, 
#                         href, 
#                         path_to_save
#                         )
#                     wb.unzip_Z(path_in)
#     #     try:
#     #         download_orbit(
#     #             dn, 
#     #             const = const, 
#     #             network = network, 
#     #             root = root
#     #             )
#     #     except:
#     #         continue 
        
#     # if const == 'igv':
#     #     rename_igv(year, root = root)
        
#     return None 

# # year = 2009
# # download_orbits_dialy(
# #         year = year, 
# #         root = 'E:\\',
# #         const = 'igv', 
# #         )


import os
import shutil
import datetime as dt
import pandas as pd

import Webscrape as wb
import GNSS as gs
import base as b


INFOS = {
    "igs":   "https://igs.bkg.bund.de/root_ftp/IGS/products/",
    "igs2":  "https://files.igs.org/pub/",
    "garner":"http://garner.ucsd.edu/pub/products/",
}

# regra: (subdir_builder, filename_builder, postprocess_fn)
# subdir_builder recebe (week, dn), filename_builder recebe (week, dow, dn, doy_str)
PRODUCTS = {
    ("igs", "igr"):   (lambda week, dn: f"orbits/{week}/",
                      lambda week, dow, dn, doy: f"igr{week}{dow}.sp3.Z",
                      None),

    ("igs", "igl"):   (lambda week, dn: f"glo_orbits/{week}/",
                      lambda week, dow, dn, doy: f"igl{week}{dow}.sp3.Z",
                      None),

    ("igs", "igv"):   (lambda week, dn: f"orbits/{week}/",
                      lambda week, dow, dn, doy: f"igv{week}{dow}_00.sp3.Z",
                      "rename_igv"),

    ("igs", "igs"):   (lambda week, dn: f"orbits/{week}/",
                      lambda week, dow, dn, doy: f"igs{week}{dow}.sp3.Z",
                      None),

    ("igs", "cod"):   (lambda week, dn: f"orbits/{week}/",
                      lambda week, dow, dn, doy: f"cod{week}{dow}.eph.Z",
                      None),

    ("igs", "com"):   (lambda week, dn: f"mgex/{week}/",
                      lambda week, dow, dn, doy: f"com{week}{dow}.eph.Z",
                      None),

    # IGS "pub" alternativo
    ("igs2", "igr"):  (lambda week, dn: f"orbits/{week}/",
                      lambda week, dow, dn, doy: f"igr{week}{dow}.sp3.Z",
                      None),

    ("igs2", "igl"):  (lambda week, dn: f"glonass/products/{week}/",
                      lambda week, dow, dn, doy: f"igl{week}{dow}.sp3.Z",
                      None),

    # Garner
    ("garner", "igv"): (lambda week, dn: f"{week}/",
                        lambda week, dow, dn, doy: f"igv{week}{dow}_00.sp3.Z",
                        "rename_igv"),
    
    ("garner", "igl"):  (lambda week, dn: f"/{week}/",
                      lambda week, dow, dn, doy: f"igl{week}{dow}.sp3.Z",
                      None),
    
    ("garner", "igr"):  (lambda week, dn: f"/{week}/",
                      lambda week, dow, dn, doy: f"igr{week}{dow}.sp3.Z",
                      None),

    ("garner", "esa"): (lambda week, dn: f"{week}/",
                        lambda week, dow, dn, doy: f"esa{week}{dow}.sp3.Z",
                        None),
}


def ensure_orbit_dirs(year, root="E:\\", const="igr"):
    path = gs.paths(year, doy=0, root=root)
    b.make_dir(path.orbit_base)
    b.make_dir(path.orbit(const=const))
    return path


def orbit_url(dn, network="igs", const="igr"):
    """
    Retorna (filename, url_base) para uma data dn.
    """
    key = (network, const)
    if key not in PRODUCTS:
        raise ValueError(f"Sem regra para network={network!r}, const={const!r}")

    week, dow = gs.dn2gpsweek(dn)
    doy = dn.strftime("%j")

    subdir_builder, filename_builder, post = PRODUCTS[key]
    # print(INFOS[network], subdir_builder(week, dn))
    url = INFOS[network] + subdir_builder(week, dn)
    filename = filename_builder(week, dow, dn, doy)

    return filename, url, post


def igv_sp3_name(fn: str) -> str:
    # remove _00 e .Z para o nome final esperado após unzip/rename
    return fn.replace("_00", "").replace(".Z", "")


def rename_igv_folder(folder):
    # renomeia igvxxxxd_00.sp3 -> igvxxxxd.sp3
    for fn in os.listdir(folder):
        if "_00" in fn:
            src = os.path.join(folder, fn)
            dst = os.path.join(folder, fn.replace("_00", ""))
            if not os.path.exists(dst):
                os.rename(src, dst)


def last_download_dn(folder, year):
    """
    Tenta inferir último dia baixado olhando arquivos tipo igrWWWWD...
    Se falhar, retorna 1/jan.
    """
    fns = [fn for fn in os.listdir(folder) if len(fn) >= 8]
    dns = []
    for fn in fns:
        try:
            gpsweek, dayofweek = int(fn[3:7]), int(fn[7:8])
            dns.append(gs.gpsweek2dn(gpsweek, dayofweek))
        except Exception:
            continue

    return max(dns) if dns else dt.datetime(year, 1, 1)


def download_orbits_daily(
        year=2022, root="E:\\", 
        const="igv", network="garner",
        resume=True, verbose=True):
    """
    Baixa órbitas diariamente para um ano inteiro (bissexto automático),
    descompacta e renomeia quando necessário.
    """
    # prepara pastas
    path_year = ensure_orbit_dirs(year, root=root, const=const)
    out_dir = path_year.orbit(const=const)

    # define intervalo do ano
    start = dt.datetime(year, 1, 1)
    end   = dt.datetime(year, 12, 31)

    if resume:
        start = last_download_dn(out_dir, year)
        # começa no próximo dia (evita repetir)
        start = (start + dt.timedelta(days=1)).replace(
            hour=0, minute=0, second=0)

    for dn in pd.date_range(start, end, freq="D"):
        fn, url, post = orbit_url(dn, network=network, const=const)

        # nome final esperado (após unzip)
        expected = igv_sp3_name(fn) if fn.endswith(".Z") else fn.replace(".gz", "")
        expected_path = os.path.join(out_dir, expected)

        if os.path.exists(expected_path):
            continue

        # baixa: mantém seu padrão de varrer request(url)
        found = False
        for href in wb.request(url):
            if fn in href:
                found = True
                if verbose:
                    print("[download_orbit]", dn.date(), href)

                downloaded = wb.download(url, href, out_dir)

                # descompactação
                try:
                    if downloaded.endswith(".Z"):
                        wb.unzip_Z(downloaded)
                    elif downloaded.endswith(".gz"):
                        wb.unzip_gz(downloaded)
                except:
                    continue

                break

        if verbose and not found:
            print("[missing]", dn.date(), fn)

        # pós-processamento (renomear igv)
        if post == "rename_igv":
            rename_igv_folder(out_dir)

    return None

# for const in ['igr', 'igl']:
download_orbits_daily(
    year=2009, root="E:\\", 
    const= 'esa', network="garner",
    resume=True, verbose=True)
 
# dn = dt.datetime(2009,1,1)
# fn, url, post = orbit_url(dn, network="garner", const='igr')

# for href in wb.request(url):
#     print(href)