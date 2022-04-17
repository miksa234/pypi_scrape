#!/usr/bin/env python3.6

import pypi_xmlrpc
import re
import requests


def main()
    url = 'https://pypi.org/pypi/{}/json'
    packages = pypi_xmlrpc.list_packages()

    f = open('test.csv', 'w')
    f.write("package|requirement\n")

    for i, package in enumerate(packages):

        try:
            json = requests.get(url.format(package)).json()
        except:
            print("ERROR")
            continue

        try:
            needs = list(dict.fromkeys([re.sub(r' (.*)', '', d) for d in json['info']['requires_dist']]))
        except:
            f.write(f'{package}|\n')  # create standalone node
            continue

        for req in needs:
            if package == req: # avoid self loops
                continue
            else:
                f.write(f'{package}|{req}\n')
        print(package)

    f.close()

if __name__ == '__main__':
    main()
