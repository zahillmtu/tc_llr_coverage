"""Script to determine the coverage of modified LLRs in the Test Cases"""

__author__ = "Zachary Hill"
__email__ = "zachary.hill@psware.com"

import os
import re
import sys

from Tkinter import Tk
from tkFileDialog import askdirectory

RES_FILE = './coverage_results.log'

def find_require_ln(fileName):
    """Method to find the line number of the location of 'REQUIREMENTS'
    in the text documents
    If no 'REQUIREMENTS' is found will return -1, otherwise returns line number
    """

    with open(fileName, 'r') as file:
        for num, line in enumerate(file, 1):
            if 'REQUIREMENTS' in line.upper():
                return num
    return -1 # if here no requirements found

def find_requirements(fileName, fullFileName, cases_covered):
    """Method to list out the requirements covered by
    a file.
    """

    # Find requirements section
    require_ln = find_require_ln(fullFileName)
    if require_ln == -1:
        print('ERROR: Could not find LLR requirements in file %s' % fileName)

    # Read in data
    with open(fullFileName, 'r') as f:
        data = f.read().splitlines(True)

    # Find all requirements
    print('\t%s' % fileName)
    requires = []
    k = 0
    checked_second = False
    while(True):
        # Search all lines under 'REQUIREMENTS' section until out of requirements
        m1 = re.search('IMMC_LLR_[0-9]+', str(data[require_ln + k]))
        if m1:
            print('\t\t%s' % m1.group(0))
            requires.append(m1.group(0))
            k = k + 1
        else:
            # Found no more requirements
            # if counter is still zero then there are no requirements
            # check another line down because some may have empty line first
            if k == 1 and checked_second:
                print('\t\tNo or improper requirements')
                break
            elif k == 0 and not checked_second:
                k = k + 1
                checked_second = True
                continue
            break

    cases_covered.extend(requires)

def main():
    """ Script to list all the LLRs under the 'REQUIREMENTS'
    section of the Test Case text files.
    """

    # Redirect output to a file
    sys.stdout = open(RES_FILE, "w")

    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    rootDir = askdirectory() # show an "Open" dialog box and return the path to the selected file
    print('Head of tree travesal selected %s' % rootDir)

    # need variables to store data
    modified = []
    cases_covered = []

    # Traverse the tree
    for dirName, subdirList, fileList in os.walk(rootDir):
        # Ignore hidden files and directories
        fileList = [f for f in fileList if not f[0] == '.']
        subdirList[:] = [d for d in subdirList if not d[0] == '.']

        print('')
        print('Found directory: %s' % dirName)
        for file in fileList:
            if file.endswith('.txt') and file.startswith('TC'):
                find_requirements(file, os.path.join(dirName, file), cases_covered)

    for req in cases_covered:
        print(req)

if __name__ == '__main__':
    main()
