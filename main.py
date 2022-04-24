#!/usr/bin/env python3

from src.interface.ui import banner
from src.wsob.main import start

from argparse import ArgumentParser

if __name__ == "__main__":
    banner()

    parser = ArgumentParser()
    parser.add_argument('-u', help="Check if target is vulnerable to CVE-2022-29464", required=True)
    args: str = parser.parse_args()

    start(args)