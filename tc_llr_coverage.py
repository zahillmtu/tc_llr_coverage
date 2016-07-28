"""Script to determine the coverage of modified LLRs in the Test Cases"""

__author__ = "Zachary Hill"
__email__ = "zachary.hill@psware.com"

import os
import re
import sys

from Tkinter import Tk
from tkFileDialog import askdirectory



def main():
    """ Script to list all the LLRs under the 'REQUIREMENTS'
    section of the Test Case text files.
    """

    # Redirect output to a file
    # sys.stdout = open(RES_FILE, "w")

    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    rootDir = askdirectory() # show an "Open" dialog box and return the path to the selected file
    print('Head of tree travesal selected %s' % rootDir)

    # Traverse the tree
    for dirName, subdirList, fileList in os.walk(rootDir):
        # Ignore hidden files and directories
        fileList = [f for f in fileList if not f[0] == '.']
        subdirList[:] = [d for d in subdirList if not d[0] == '.']

        print('')
        print('Found directory: %s' % dirName)
        for file in fileList:
            if file.endswith('.txt') and file.startswith('TC'):
                find_requirements(file, os.path.join(dirName, file)) # needs absolute path


if __name__ == '__main__':
    main()
