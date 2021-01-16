# Owner: Manfredi Miraula
# Date created: Jan 16 2021
# The script takes the .gz files in the folder and extract them

# import libraries
import gzip
import glob
import os.path
from pathlib import Path
import sys

source_dir, dest_dir = str(Path().absolute()), str(Path().absolute())

# we extract the .gz file within the folder. This script will extract all the gz file in the folder
for src_name in glob.glob(os.path.join(source_dir, '*.gz')):
    base = os.path.basename(src_name)
    dest_name = os.path.join(dest_dir, base[:-3])
    with gzip.open(src_name, 'rb') as infile:
        with open(dest_name, 'wb') as outfile:
            for line in infile:
                outfile.write(line)


sys.exit('Process executed and closed')

