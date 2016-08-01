"""Script to determine the coverage of modified LLRs in the Test Cases

This script will travese the specified file directory, into all sub-directories,
to determine if all of the LLRs specified are covered by the test cases in
the directory. If an LLR is not listed within any of the files, the name of the
LLR will be printed out in the 'coverage_results.log' log file.

NOTE:
    The LLRs you would like to check for need to be placed in a '.txt' file
    or '.csv'. Each LLR MUST be on a separate new line. The name of the file
    is not important.

TO RUN:
    Run the script using Python 2.7 and a dialog box will appear, select
    the root directory. A second dialog box will appear asking you to
    select a file, this is where you will select the LLR file that is
    specified above in the 'NOTE' section.

OUTPUT:
    The output of the script will be directed to 'coverage_results.log'.

"""

__author__ = "Zachary Hill"
__email__ = "zachary.hill@psware.com"

import os
import re
import sys

from Tkinter import Tk
from tkFileDialog import askdirectory
from tkFileDialog import askopenfilename

RES_FILE = './coverage_results.log'
MODIFIED_TC_FILE = './modified_tc_file.csv'

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
    requires = []
    k = 0
    checked_second = False
    while(True):
        # Search all lines under 'REQUIREMENTS' section until out of requirements
        m1 = re.search('IMMC_LLR_[0-9]+', str(data[require_ln + k]))
        if m1:
            requires.append(m1.group(0))
            k = k + 1
        else:
            # Found no more requirements
            # if counter is still zero then there are no requirements
            # check another line down because some may have empty line first
            if k == 1 and checked_second:
                break
            elif k == 0 and not checked_second:
                k = k + 1
                checked_second = True
                continue
            break

    cases_covered.extend(requires)

def gather_modified(modified, modified_file):
    """Method to retrieve the modified requirements from
    a .csv file
    """

    # Read in data
    with open(modified_file, 'r') as f:
        data = f.read().splitlines(True)

    modified.extend(data)
    return


def main():
    """ Script to list all the LLRs under the 'REQUIREMENTS'
    section of the Test Case text files.
    """

    # Redirect output to a file
    sys.stdout = open(RES_FILE, "w")

    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    rootDir = askdirectory() # show an "Open" dialog box and return the path to the selected file
    print('Head of tree travesal selected %s' % rootDir)

    Tk().withdraw()
    modified_file = askopenfilename()
    print('File of LLRs to test coverage against %s' % modified_file)

    # need variables to store data
    modified = []
    cases_covered = []

    # Traverse the tree
    for dirName, subdirList, fileList in os.walk(rootDir):
        # Ignore hidden files and directories
        fileList = [f for f in fileList if not f[0] == '.']
        subdirList[:] = [d for d in subdirList if not d[0] == '.']

        for file in fileList:
            if file.endswith('.txt') and file.startswith('TC'):
                find_requirements(file, os.path.join(dirName, file), cases_covered)

    # get modified data
    gather_modified(modified, modified_file)

    not_found = 0
    print('')
    print('The following cases are not covered in the Test Case documents:')
    # Find any requirements in modified that are not in cases_covered
    for case in modified:
        found = False
        for tc in cases_covered:
            if (str(case).strip().rstrip()) == (str(tc).strip().rstrip()):
                found = True
                break
        if not found:
            print('\t%s' % str(case).strip().rstrip())
            not_found += 1
            continue

    num_modified = len(modified)
    print('')
    print('Number of Test cases not found: %d' % not_found)
    print('Number of Test cases modified: %d' % len(modified))
    if num_modified != 0:
        print('Percent missing: %.2f%%' % ((not_found * 1.0) / num_modified * 100.0))
    else:
        print('percent missing: 0%%')

if __name__ == '__main__':
    main()
