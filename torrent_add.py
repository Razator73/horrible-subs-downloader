import logging
import os
import sys

import transmission_rpc as trpc

from horrible_torrents import wait_for_download
from set_logger import define_logger

logger = define_logger(__name__, logging.DEBUG, file_name='manual_add.log')

magnet_url = sys.argv[1]
logger.debug(f'Adding {magnet_url}')
tor_client = trpc.Client(port=os.environ['TRANSMISSION_PORT'],
                         username=os.environ['TRANSMISSION_USERNAME'],
                         password=os.environ['TRANSMISSION_PASSWORD'])

t_id = tor_client.add_torrent(magnet_url).id
logger.debug(f'Added with id={t_id}')
wait_for_download([t_id], tor_client)
logger.info(f'Successfully added torrent {magnet_url}')
