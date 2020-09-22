#!/usr/bin/env pipenv-shebang
import argparse
import logging
import os

import ezgmail
import transmission_rpc as trpc

from horrible_torrents import wait_for_download
from set_logger import define_logger

logger = define_logger(__name__, logging.INFO, file_name='manual_add.log')

arg_parser = argparse.ArgumentParser(prog='torrent_downloader', description='Add a torrent to be downloaded')
arg_parser.add_argument('magnet_url', help='The magnet URL for the torrent to be added')
args = arg_parser.parse_args()

logger.debug(f'Adding {args.magnet_url}')
try:
    tor_client = trpc.Client(port=os.environ['TRANSMISSION_PORT'],
                             username=os.environ['TRANSMISSION_USERNAME'],
                             password=os.environ['TRANSMISSION_PASSWORD'])
except KeyError:
    logger.error('The transmission credentials are not set')
    raise

torrent = tor_client.add_torrent(args.magnet_url)
logger.debug(f'Added with id={torrent.id}')
wait_for_download([torrent.id], tor_client)
logger.info(f'Successfully added torrent {args.magnet_url}')

try:
    ezgmail.init(tokenFile=os.environ.get('GMAIL_TOKEN', 'token.json'),
                 credentialsFile=os.environ.get('GMAIL_CREDENTIALS', 'credentials.json'))
    ezgmail.send(os.environ.get('GMAIL_RECIPIENT', ezgmail.EMAIL_ADDRESS),
                 'Torrent Downloaded',
                 'Hey,\n\n The torrent you set to be downloaded has finished. Files downloaded:\n\n\t' +
                 '\n\t'.join([file['name'] for file in torrent.files().values()]) +
                 '\n\nThanks')
except KeyError:
    logger.error('Failed to send the email due to creds not being set')
    raise
