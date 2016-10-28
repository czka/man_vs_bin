#!/usr/bin/env python

import subprocess
import re


class Package(object):
    def __init__(self, pname):
        self.pname = pname
        self.paths = subprocess.check_output(['pacman', '-Qlq', self.pname]).\
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
    import argparse

    parser = argparse.ArgumentParser(
        description="Help identify binaries/scripts and man pages missing each "
                    "other in an Arch Linux package. This tool uses some naive "
                    "heuristics and only gives the user a hint, not a solid "
                    "truth.", add_help=False)

    group = parser.add_argument_group("Arguments")
    group.add_argument("--help", action='store_true',
                       help="Show this help message and exit.")

    args = parser.parse_known_args()
    group.add_argument("--package",  metavar='PACKAGE', dest='pname',
                       type=str, help="Input package name.", required=True)

    if args[0].help:
        parser.exit(parser.print_help())
    else:
        args = parser.parse_args()
        package = Package(args.pname)
        mans = package.find_man_paths()
        bins = package.find_bin_paths()

        if not mans and not bins:
            print("Seems like it's all in order.\n")
        else:
            if mans - bins:
                print("Possible man pages that might be missing their "
                      "executables:\n%s\n" % str(mans - bins)[1:-1])
            if bins - mans:
                print("Possible executables that might be missing their man "
                      "pages:\n%s\n" % str(bins - mans)[1:-1])
