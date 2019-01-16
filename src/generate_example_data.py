#!/usr/bin/env python3
"""Generates example text file filled with random data."""

import argparse
import random
import string


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('length', type=int)
    args = parser.parse_args()
    data = ''.join(random.choices(string.printable, k=args.length))
    print(data)


if __name__ == '__main__':
    main()
