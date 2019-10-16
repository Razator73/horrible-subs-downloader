import logging
import os
import sys
from pathlib import Path

import bs4
import transmission_rpc as trpc
from selenium import webdriver


def get_horrible_sub_elements(show_url):
    url = f'https://horriblesubs.info/shows/{show_url}/'
    logger.info(url)
    browser = webdriver.Chrome()
    browser.get(url)
    soup = bs4.BeautifulSoup(browser.page_source, features='lxml')
    browser.quit()

    return soup.select('div[class="rls-link link-1080p"][id]')


def add_torrents(show_name, link_elements):
    try:
        tor_client = trpc.Client(port=os.environ['TRANSMISSION_PORT'],
                                 username=os.environ['TRANSMISSION_USERNAME'],
                                 password=os.environ['TRANSMISSION_PASSWORD'])
    except KeyError:
        logger.exception('Environment variables not set correctly')
        sys.exit(1)

    ids_path = Path(__file__).parent / 'show-logs' / f'{show_name}.log'
    ids_path.touch(exist_ok=True)

    with open(ids_path) as f:
        ids = [x.strip() for x in f.readlines()]

    added_torrents = []

    for elem in link_elements:
        link_id = elem.attrs['id']
        if link_id not in ids:
            logger.info(link_id)
            with open(ids_path, mode='a') as f:
                f.write(f'{link_id}\n')
            magnet_url = elem.select_one('a[title="Magnet Link"]').attrs['href']
            # added_torrents.append(tor_client.add_torrent(magnet_url))

    return added_torrents


if __name__ == '__main__':
    logger = logging.Logger(__name__)
    logger.setLevel(logging.WARNING)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('\n%(asctime)s - %(levelname)s - %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # noinspection PyBroadException
    try:
        check_args = True
        show = sys.argv[1] if check_args else 'sword-art-online-alicization-war-of-underworld'
        logger.info(show)
        elements = get_horrible_sub_elements(show)
        add_torrents(show, elements)
    except Exception:
        logger.exception('Failed to get all torrents')
        sys.exit(1)
