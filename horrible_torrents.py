import os
import sys
import time
from pathlib import Path

import bs4
import transmission_rpc as trpc
from pyvirtualdisplay import Display
from selenium import webdriver

from set_logger import define_logger

logger = define_logger(__name__)


def get_horrible_sub_elements(show_url):
    url = f'https://horriblesubs.info/shows/{show_url}/'
    logger.debug(f'Checking at {url}')
    display = Display(visible=False)
    display.start()
    browser = webdriver.Chrome()
    browser.get(url)
    soup = bs4.BeautifulSoup(browser.page_source, features='lxml')
    browser.quit()
    display.stop()

    return soup.select('div[class="rls-link link-1080p"][id]')


def add_torrents(show_name, link_elements, client):

    try:
        ids_path = Path(__file__).parent / 'show-logs' / f'{show_name}.log'
    except NameError:
        ids_path = Path('show-logs') / f'{show_name}.log'
    ids_path.touch(exist_ok=True)

    with open(ids_path) as f:
        ids = [x.strip() for x in f.readlines()]

    added_torrent_ids = []

    for elem in link_elements:
        link_id = elem.attrs['id']
        if link_id not in ids:
            logger.info(f'New episode {show_name} - {link_id}')
            with open(ids_path, mode='a') as f:
                f.write(f'{link_id}\n')
            magnet_url = elem.select_one('a[title="Magnet Link"]').attrs['href']
            added_torrent_ids.append(client.add_torrent(magnet_url).id)

    return added_torrent_ids


def wait_for_download(ids, client):
    for t_id in ids:
        while (torrent := client.get_torrent(t_id)).status == "downloading":
            try:
                sleep_secs = min([max([5, torrent.eta.seconds / 2]), 300])
            except ValueError:
                sleep_secs = 60
            logger.debug(f'Sleeping for {sleep_secs} seconds')
            time.sleep(sleep_secs)


if __name__ == '__main__':

    # noinspection PyBroadException
    try:
        check_args = True
        show = sys.argv[1] if check_args else 'sword-art-online-alicization-war-of-underworld'
        logger.debug(f'Getting new episodes for {show}')
        elements = get_horrible_sub_elements(show)

        try:
            tor_client = trpc.Client(port=os.environ['TRANSMISSION_PORT'],
                                     username=os.environ['TRANSMISSION_USERNAME'],
                                     password=os.environ['TRANSMISSION_PASSWORD'])
        except KeyError:
            logger.exception('Environment variables not set correctly')
            sys.exit(1)

        torrent_ids = add_torrents(show, elements, tor_client)
        logger.debug(f'Torrent ids - {torrent_ids}')
        wait_for_download(torrent_ids, tor_client)
    except Exception:
        logger.exception('Failed to get all torrents')
        sys.exit(1)
