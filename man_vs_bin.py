#!/usr/bin/env python

import subprocess
import re


class Package(object):
    """A rather naive, but useful (at least to me) tool to help identify
    binaries/scripts and man pages missing each other in an Arch Linux
    package."""

    def __init__(self, name):
        self.name = name
        self.paths = subprocess.check_output(['pacman', '-Qlq', self.name]).\
                     decode('UTF-8').split('\n')[:-1]

    def find_paths(self, regex):
        items = set()
        for item in self.paths:
            if regex.search(item):
                items.add(item.split(sep='/')[-1].split(sep='.')[0])
        return items

    def find_man_paths(self):
        regex = re.compile(r'/man/\S+\.\d+')
        return self.find_paths(regex)

    def find_bin_paths(self):
        regex = re.compile(r'/bin/\S+')
        return self.find_paths(regex)

if __name__ == '__main__':
    # package_name = sys.argv[1]
    package_name = 'gdal'
    package = Package(package_name)
    mans = package.find_man_paths()
    bins = package.find_bin_paths()

    print("Example usage - print GDAL package man pages that might be missing "
          "their respective executables:")
    print(mans - bins)
    print()
    print("And vice-versa:")
    print(bins - mans)
