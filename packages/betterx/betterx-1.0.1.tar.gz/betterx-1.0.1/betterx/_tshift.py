"""
usage: tshift [-h] [-o OUTPUT] [-n NUMBER] [-v] file

replaces all tab characters in a file with spaces

positional arguments:
  file           file to read for tab characters

optional arguments:
  -h, --help     show this help message and exit
  -o OUTPUT      write tab replaced file into a different file
  -n NUMBER      number of spaces to convert tab to
  -v, --version  show program's version number and exit
"""
import os

from typing import Tuple


def tshift(path: str, space_number: int = 4, output: str = '') -> Tuple[bool, str]:
    """
    reads file located at path
    argument and converts every
    tab character read into
    space times the number of 2ns arg
    """

    if space_number <= 0:
        return False, 'space number should be a non zero positive number'

    exists = os.path.isfile(path)
    if exists:

        # read old file into text
        old_file = open(path, 'r')
        text = old_file.read()

        # replace all tab characters
        # with spaces and close the file
        text = text.replace('\t', ' ' * space_number)
        old_file.close()

        # remove buffer from memory
        del old_file

        # open new file and
        # write the text to it
        if len(output) > 0:
            new_file = open(output, 'w+')
        else:
            new_file = open(path, 'w+')

        new_file.write(text)
        new_file.close()

        return True, ''
    else:
        return False, 'file "{}" does not exist'.format(os.path.abspath(path))
