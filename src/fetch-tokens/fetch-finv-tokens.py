#!/usr/bin/env python3

# Reference: test_download_masters.py in github.com/Shoonya-Dev/ShoonyaApi-py

from datetime import datetime
import requests
import zipfile
import sys
import os
import errno
import argparse

root = 'https://shoonya.finvasia.com/'
masters = ['NSE_symbols.txt.zip',
           'BSE_symbols.txt.zip',
           'NFO_symbols.txt.zip',
           'CDS_symbols.txt.zip',
           'MCX_symbols.txt.zip']


if __name__=="__main__":

    # Add support to parse command-line arguments and also show usage
    parser = argparse.ArgumentParser(description='Fetch an exchange-wise list of scrips and corresponding tokens.')
    parser.add_argument('-o', '--output-dir', dest='output_dir', nargs=1, default=None,
                                        help='Location to create the directory with the lists.')
    args = parser.parse_args()

    # If the user has NOT explicitly specified an output directory,
    # create an output sub-directory based on the current time.
    if args.output_dir:
        output_dir = args.output_dir[0]
    else:
        output_dir = 'finv-tokens-' + datetime.now().strftime("%d%b%Y-%H%M%S")

    # Attempt to create the local output directory
    try:
        os.makedirs(output_dir)
        os.chdir(output_dir)
    except FileExistsError:
        pass
    except:
        print(f'Failed to create directory "{output_dir}"! Aborted Execution.')
        sys.exit(errno.ENOENT)

    # Attempt to fetch, save, and extract all the various known lists
    for zip_file in masters:

        # Fetch a source...
        url = root + zip_file
        print(f'Downloading "{url}" ...')
        try:
            r = requests.get(url, allow_redirects=True)
        except:
            sys.exit(errno.EBUSY)

        # ...Save it as a temporary file...
        print(f'Saving as "{zip_file}"...')
        open(zip_file, 'wb').write(r.content)
        file_to_extract = zip_file.split()

        # Extract the contents of the temporary zip file.
        # If successful, cleanup the temporary zip file.
        try:
            with zipfile.ZipFile(zip_file) as z:
                z.extractall()
                print('Extracted', zip_file)

                os.remove(zip_file)
                print(f'Cleaned-up "{zip_file}"')

        except:
            print('Invalid zip file!')
            sys.exit(errno.EINVAL)

    # Successful execution
    print(f'Sucessfully downloaded and saved within "{output_dir}"')
    sys.exit(0)
