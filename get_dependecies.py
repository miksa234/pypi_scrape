#!/usr/bin/env python3.6

import pypi_xmlrpc
import re
import requests
from datetime import datetime


def main():
    url = 'https://pypi.org/pypi/{}/json'
    packages = pypi_xmlrpc.list_packages()

    path = './data/'
    files = {}

    for i, package in enumerate(packages):
        try:
            json = requests.get(url.format(package)).json()
        except:
            print("ERROR")
            continue

        catch = True; j = 0
        while catch:
            try:
                timestr = list(json['releases'].items())[j][1][0]['upload_time']
                release = datetime.strptime(timestr, "%Y-%m-%dT%H:%M:%S")
                catch = False
            except:
                j += 1
        try:
            files[f'{release.year}-{release.month}'].closed
        except:
            files[f'{release.year}-{release.month}'] = open(path + f'{release.year}-{release.month}.csv', "w")
            files[f'{release.year}-{release.month}'].write('package|requirement\n')

        try:
            needs = list(dict.fromkeys([re.sub(r' (.*)', '', d) for d in json['info']['requires_dist']]))
        except:
            files[f'{release.year}-{release.month}'].write(f'{package}|\n')  # create standalone node
            continue

        for req in needs:
            if package == req: # avoid self loops
                continue
            else:
                files[f'{release.year}-{release.month}'].write(f'{package}|{req}\n')
        print(package)

    for file in files:
        files[file].close()


if __name__ == '__main__':
    main()
