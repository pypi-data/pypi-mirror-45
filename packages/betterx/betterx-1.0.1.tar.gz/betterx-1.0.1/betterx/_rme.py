"""
usage: rme [-h] [-d DIRECTORY] [-s] [-v] files [files ...]

remove every file except for the ones mentioned

positional arguments:
  files          files to save or not remove

optional arguments:
  -h, --help     show this help message and exit
  -d DIRECTORY   directory to remove files from
  -s             supress errors for files not found
  -v, --version  show program's version number and exit
"""
import os
import shutil
import argparse

from typing import List, Tuple

DIR_FILES: List[str] = []


def rme(
    preserve_files: List[str], directory: str = '.', supress: bool = False
) -> Tuple[bool, str]:
    """
    takes three arguments 
        preserve_files : a list of files / directories to be passed and not deleted
        directory : location to loop through files / directories and delete or NOT delete files
        supress : a boolean value -
            if False - passes without any breaks
            if True - raises FileNotFoundError if preserve_files are not found in directory
    """
    global DIR_FILES

    DIR_FILES = os.listdir(directory)
    files = [
        os.path.abspath('{}/{}'.format(directory, file))
        for file in DIR_FILES
        if file not in preserve_files
    ]

    if not supress:
        for file in preserve_files:
            if file not in DIR_FILES:
                raise FileNotFoundError(
                    'file {} doesn\'t exist in directory {}'.format(
                        file, os.path.abspath(directory)
                    )
                )

    for file in files:
        try:
            if os.path.isdir(file):
                # os.rmdir was used earlier but due to
                # errors being raised when a directory
                # was not empty, shutil.rmtree was utilized
                shutil.rmtree(file)
                continue
            os.remove(file)
        except KeyboardInterrupt:
            return False, 'manual exit'
        except Exception as e:
            return False, str(e)
    return True, ''
