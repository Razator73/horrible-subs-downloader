import os
import sys
import time

import transmission_rpc as trpc

tor_client = trpc.Client(port=os.environ['TRANSMISSION_PORT'],
                         username=os.environ['TRANSMISSION_USERNAME'],
                         password=os.environ['TRANSMISSION_PASSWORD'])

t_id = sys.argv[1]
while (torrent := tor_client.get_torrent(t_id)).status == "downloading":
    try:
        sleep_secs = min([max([5, torrent.eta.seconds / 2]), 300])
    except ValueError:
        sleep_secs = 60
    print(f'Sleeping for {sleep_secs} seconds')
    time.sleep(sleep_secs)
torrent.stop()
print('Done')
