import os
from glob import glob
def file_cleanup():
    files = glob('images/*.png')
    for f in files:
        os.remove(f)
