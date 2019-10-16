import os
import shutil
import sys
from pathlib import Path


download_dir = Path(os.environ['DOWNLOAD_DIR'])
destination_dir = Path(os.environ['DESTINATION_DIR'])

check_args = True
pattern = sys.argv[1] if check_args else 'NO FILES SHOULD MATCH THIS'

copied = [x.name for x in destination_dir.glob(pattern)]
for file in [x for x in download_dir.glob(pattern) if x.name not in copied]:
    shutil.copy(file, destination_dir)
