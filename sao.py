import os
from pathlib import Path

import bs4
import transmission_rpc as trpc
from selenium import webdriver


ids_path = Path(__file__).parent / 'ids_loaded.log'
ids_path.touch(exist_ok=True)

sao_url = 'https://horriblesubs.info/shows/sword-art-online-alicization-war-of-underworld/'
browser = webdriver.Chrome()
browser.get(sao_url)
soup = bs4.BeautifulSoup(browser.page_source)
browser.quit()

with open(ids_path) as f:
    ids = [x.strip() for x in f.readlines()]

elements = soup.select('div[class="rls-link link-1080p"][id]')
tor_client = trpc.Client(port=os.environ['TRANSMISSION_PORT'],
                         username=os.environ['TRANSMISSION_USERNAME'],
                         password=os.environ['TRANSMISSION_PASSWORD'])

for elem in elements:
    link_id = elem.attrs['id']
    if link_id not in ids:
        print(link_id)
        with open(ids_path, mode='a') as f:
            f.write(f'{link_id}\n')
        magnet_url = elem.select_one('a[title="Magnet Link"]').attrs['href']
        tor_client.add_torrent(magnet_url)
