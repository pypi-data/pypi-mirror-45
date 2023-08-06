"""
usage: lsx [-h] [-n NUMBER] [-t TIME] [-i] [-v] [directory]

updates the listing of files after some interval

positional arguments:
  directory       directory to be listed after interval

optional arguments:
  -h, --help      show this help message and exit
  -n NUMBER       number of times to list directory
  -t TIME         number of seconds to update listing
  -i, --infinity  infinity mode - stops only with manual user exit
  -v, --version   show program's version number and exit
"""
import os

from typing import List


def lsx(path: str) -> List:
    return os.listdir(path)
