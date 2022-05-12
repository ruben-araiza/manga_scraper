import os
from datetime import datetime
from pathlib import Path
from re import search
from typing import Dict, List


from bs4 import BeautifulSoup as bs
from requests import get
from requests.utils import urlparse


from .settings import TITLE_PATTERN
from .utils import progress_bar, sanitize_name

def get_structured_urls(manga_path : str, verbose=True) -> List:

    parsed_url = urlparse(manga_path)
    site_hostname = parsed_url.scheme + '://' + parsed_url.hostname

    response = get(manga_path)
    if response.status_code == 200:
        soup = bs(response.content, 'html.parser')
    else:
        raise Exception('request failed')

    
    manga_name = soup.find('div', class_='story-info-right').find('h1').text
    if manga_name is None:
        raise Exception('failed to get manga name')

    chapter_element_list = soup.find('ul', class_="row-content-chapter").find_all('a')
    if chapter_element_list is None:
        raise Exception('failed to get chapter list')
    
    if verbose:
        print(f"Getting {manga_name} url lists")

    chapter_list_length = len(chapter_element_list)
    chapter_list = []
    for index, link in enumerate(chapter_element_list):

        response = get(site_hostname + link['href'])
        chapter_soup = bs(response.content, 'html.parser')
        
        re_result = search(TITLE_PATTERN, link['title'])
        chapter_list.append(
            {
                'title': 'no title' if re_result.group(3) is None else re_result.group(3),
                'chapter': re_result.group(1),
                'path': link['href'],
                'image_urls': [img['data-src'] for img in chapter_soup.find('div', class_='container-chapter-reader').find_all('img')]

            }
        )
        if verbose:
            progress_bar(index + 1, chapter_list_length, prefix='Scrapping', sufix='Scraped!')
    result = {
        'name': manga_name,
        'chapter_list': chapter_list
    }
    return result


def download_manga_images(chapter_list : Dict, download_dir=None, verbose=True) -> None:
    
    if download_dir is not None:
        download_path = Path(download_dir)
    else:
        download_path = Path.cwd()

    sanitized_dir_name = sanitize_name(chapter_list["name"])
    # create download dir
    content_path =  download_path / sanitized_dir_name
    # do something if the directory already exists
    content_path.mkdir(exist_ok = True)
    # Maybe add a file with a timestamp log

    if verbose:
        print(f"Downloading {chapter_list['name']} files to '{content_path}'")

    chapter_list_lenght = len(chapter_list['chapter_list'])

    for chapter_index, chapter in enumerate(chapter_list['chapter_list']):
        # prepare directory for the chapter
        sanitized_dir_name = sanitize_name(f'{chapter["chapter"]}_[{chapter["title"]}]')

        chapter_directory_path = content_path / sanitized_dir_name
        chapter_directory_path.mkdir()

        chapter_images_lenght = len(chapter['image_urls'])
        for image_index, url in enumerate(chapter['image_urls']):
            # filename will follow <index + 1>_<timestamp>.jpg
            timestamp = datetime.now().strftime('%Y%m%d')
            filename =  sanitize_name(f'{chapter["chapter"]}_{image_index}_{timestamp}.jpg')
            
            response = get(url)
            if response.status_code == 200:
                with open(chapter_directory_path / filename, 'wb') as image:
                    for chunk in response:
                        image.write(chunk)

            if verbose:
                pre = f"Chapter {chapter['chapter']}"
                progress_bar(image_index + 1, chapter_images_lenght, prefix=pre, sufix='Done')

