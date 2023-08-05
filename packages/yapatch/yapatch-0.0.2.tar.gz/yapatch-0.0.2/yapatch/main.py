import argparse
import os
import sys

from yapatch.patch import patch_files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', type=int)
    parser.add_argument('-d', default=os.getcwd())

    args = parser.parse_args()
    diff_text = sys.stdin.read()
    patch_files(diff_text, args.d, args.p)
