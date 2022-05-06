from datetime import datetime
from pprint import pprint
from pathlib import Path
import json


from .scraper import *
from .utils import *


def scrap(manga_url, download_dir=None, verbose=False, cache_path=None):

    manga_info = get_structured_urls(manga_url, verbose=verbose)
    
    if cache_path is not None:
        cache_path = Path(cache_path)
        if cache_path.is_dir():
            timestamp = datetime.now().strftime('%Y%m%d')
            file_name = f"{sanitize_name(manga_info['name'])}_info_{timestamp}.json"

            with open(file_name, 'w+') as f:
                json.dump(manga_info, f)

    download_manga_images(manga_info, download_dir=download_dir, verbose=verbose)


def scrap_from_file(cache_path, download_dir=None, verbose=False):

    with open(cache_path, 'r') as file:
        manga_info = json.load(file)
    
    download_manga_images(manga_info, download_dir=download_dir, verbose=verbose)

