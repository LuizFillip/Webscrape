from __future__ import annotations
import datetime as dt
from pathlib import Path
from typing import Iterable, Sequence, Tuple, Union, Optional, List
import pandas as pd
from tqdm import tqdm
from base import make_dir
import scrap as wb
 

# ----------------------------
# Config / helpers
# ----------------------------

SITES = {
    "fortaleza": "FZA0M",
    "sao_luis": "SAA0K",
    "belem": "BLJ03",
    "cachoeira": "CAJ2M",
    "santa_maria": "SMK29",
    "boa_vista": "BVJ03",
    "campo_grande": "CGK21",
}


def sites_codes(site: str) -> str:
    try:
        return SITES[site]
    except KeyError as e:
        raise KeyError(f"Site desconhecido: {site}. Opções: {list(SITES)}") from e


def folder_name(dn: dt.datetime, site: str, flat: bool = False) -> str:
    """
    Ex:
      flat=False -> \\YYYY\\YYYYMMDDXX
      flat=True  -> YYYYMMDDXX
    onde XX = 2 letras do código do site (ex: FZ, SA, ...)
    """
    ext = sites_codes(site)[:2].upper()
    return dn.strftime(f"%Y%m%d{ext}") if flat else dn.strftime(f"{Path(str(dn.year)) / (dn.strftime(f'%Y%m%d{ext}'))}")


def fn2dt(filename: str) -> dt.datetime:
    """
    Ex: 'FZA0M_2015365210000.SAO' -> datetime pelo padrão %Y%j%H%M%S.
    """
    # mais robusto que split fixo
    parts = filename.split("_", 1)
    if len(parts) != 2:
        raise ValueError(f"Nome de arquivo inesperado: {filename}")

    date_part = parts[1].split(".", 1)[0]  # remove extensão
    return dt.datetime.strptime(date_part, "%Y%j%H%M%S")


def periods_by_range(start: dt.datetime, hours: float = 24, freq: str = "10min") -> pd.DatetimeIndex:
    end = start + dt.timedelta(hours=hours)
    return pd.date_range(start, end, freq=freq)


def periods_by_freq(
        start: dt.datetime, 
        end: Optional[dt.datetime] = None, 
        freq: str = "1D"
        ) -> pd.DatetimeIndex:
    """
    Range por frequência. Se end=None, gera 1 ano a partir do start.
    """
    
    if end is None:
        end = start + dt.timedelta(days=365)
    return pd.date_range(start, end, freq=freq)


def create_folder_by_date(
        start: dt.datetime, 
        site: str, 
        root: Union[str, Path] = "D"
        ) -> Path:
    """
    Cria: <root>:/ionogram/YYYY/YYYYMMDDXX
    """
    root = Path(f"{root}:\\") if isinstance(root, str) and len(root) == 1 else Path(root)
    base_dir = root / "ionogram" / str(start.year)
    make_dir(str(base_dir))
    save_in = base_dir / folder_name(start, site=site, flat=True)
    make_dir(str(save_in))
    return save_in


def _normalize_ext(ext: Union[str, Sequence[str]]) -> List[str]:
    if isinstance(ext, str):
        return [ext]
    return list(ext)


# ----------------------------
# Web listing / filtering
# ----------------------------

def filter_extensions(
    dn: dt.datetime,
    site: str = "sao_luis",
    ext: Union[str, Sequence[str]] = ("SAO", "RSF"),
    ) -> Tuple[str, List[str]]:
    """
    Retorna (url, [filenames]) para o timestamp dn.
    """
    exts = _normalize_ext(ext)

    url = wb.embrace_url(dn, site=site, inst="ionosonde")

    files_filtered: List[str] = []
    for link in wb.request(url):
        # ignorar XML
        if "XML" in link.upper():
            continue
        if any(e in link for e in exts):
            files_filtered.append(link)

    return url, files_filtered


# ----------------------------
# Download routine
# ----------------------------

def download_in_day(
        dn_py, site, ext, 
        save_in,
        strict_timestamp_match: bool = True
        ):
    url, files = filter_extensions(dn_py, site=site, ext=ext)
    
    for filename in files:
        out_path =  Path(save_in) / filename
        if out_path.exists():
            continue

        if strict_timestamp_match:
            try:
                if fn2dt(filename) != dn_py:
                    continue
            except ValueError:
                # nome não bate padrão -> ignora
                continue

        try:
            wb.download(url, filename, str(save_in))
            
        except Exception:
            # se quiser logar, coloque print/ logger aqui
            continue
        
def download_ionograms(
    periods: Iterable[dt.datetime],
    site: str = "sao_luis",
    ext: Union[str, Sequence[str]] = ("SAO", "RSF"),
    root_drive: Union[str, Path] = "D",
    strict_timestamp_match: bool = True,
    save_in =  None
) -> None:
    """
    Baixa ionogramas para cada datetime em `periods`:
    - lista arquivos no servidor
    - filtra por extensão
    - opcionalmente baixa só se fn2dt(filename) == dn
    - salva em pasta por ano/data+site
    """
    if not isinstance(periods, dt.datetime):
        start = periods[0].to_pydatetime()
        
    if save_in is None:
        save_in = create_folder_by_date(start, site=site, root=root_drive)

    if isinstance(periods, dt.datetime):
        dn_py = periods
        download_in_day(
                dn_py, site, ext, 
                save_in,
                strict_timestamp_match = True
                )
    else:
        periods = pd.DatetimeIndex(periods)
        desc = f"{start:%Y-%m-%d} - {site}"
        for dn in tqdm(periods, desc=desc):
            dn_py = dn.to_pydatetime()
            
            download_in_day(
                    dn_py, site, ext, 
                    save_in,
                    strict_timestamp_match = True
                    )

        


# ----------------------------
# Examples / entrypoints
# ----------------------------
 
def download_years_fixed_hours(year_start: int = 2015, year_end: int = 2022, site: str = "fortaleza", hours=(21, 22)):
    for year in range(year_start, year_end + 1):
        for hour in hours:
            dn = dt.datetime(year, 1, 1, hour)
            periods = periods_by_freq(dn, freq="1D")
            download_ionograms(periods, site=site, ext=("SAO",))

def download_fixed_time_over_year(year):
    start = dt.datetime(year, 1, 1, 22)
    save_in = Path(f'D:\\database\\fza\\{start.year}\\')
    make_dir(save_in)
    for dn in periods_by_freq(start):
        print('Downloading', dn.strftime('%Y%m%d'))
        download_ionograms(
            dn, 
            site = 'fortaleza', 
            ext = 'SAO', 
            save_in = save_in
            )
        
for year in range(2013, 2025):
    download_fixed_time_over_year(year)