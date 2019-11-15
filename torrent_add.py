import logging
import os
import sys

import ezgmail
import transmission_rpc as trpc

from horrible_torrents import wait_for_download
from set_logger import define_logger

logger = define_logger(__name__, logging.INFO, file_name='manual_add.log')

magnet_url = sys.argv[1]
logger.debug(f'Adding {magnet_url}')
tor_client = trpc.Client(port=os.environ['TRANSMISSION_PORT'],
                         username=os.environ['TRANSMISSION_USERNAME'],
                         password=os.environ['TRANSMISSION_PASSWORD'])

torrent = tor_client.add_torrent(magnet_url)
logger.debug(f'Added with id={torrent.id}')
wait_for_download([torrent.id], tor_client)
logger.info(f'Successfully added torrent {magnet_url}')
ezgmail.init(tokenFile=os.environ.get('GMAIL_TOKEN', 'token.json'),
             credentialsFile=os.environ.get('GMAIL_CREDENTIALS', 'credentials.json'))
ezgmail.send(os.environ.get('GMAIL_RECIPIENT', ezgmail.EMAIL_ADDRESS),
             'Torrent Downloaded',
             'Hey,\n\n The torrent you set to be downloaded has finished. Files downloaded:\n\n\t' +
             '\n\t'.join([file['name'] for file in torrent.files().values()]) +
             '\n\nThanks')
