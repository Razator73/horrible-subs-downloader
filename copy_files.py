import os
import shutil
import sys
from pathlib import Path

import ezgmail

from set_logger import define_logger

logger = define_logger(__name__)


def show_files(pattern):
    try:
        download_dir = Path(os.environ['DOWNLOAD_DIR'])
        destination_dir = Path(os.environ['DESTINATION_DIR'])
    except KeyError:
        logger.exception('Failed to pull environment variables')
        sys.exit(1)

    copied = [x.name for x in destination_dir.glob(pattern)]
    for file in [x for x in download_dir.glob(pattern) if x.name not in copied]:
        logger.info(f'Copying {file}...')
        shutil.copy(file, destination_dir)
        ezgmail.send('ryan.t.scott73@gmail.com', 'Added file to FTP',
                     'The following file was successfully added to the ftp:\n\n'
                     f'{file.name}\n\n'
                     'Thanks,')


if __name__ == '__main__':
    check_args = True
    show_pattern = f'*{sys.argv[1]}*' if check_args else 'NO FILES SHOULD MATCH THIS'
    show_files(show_pattern)
