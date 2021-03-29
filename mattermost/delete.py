#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
from os.path import isfile,isdir,join,dirname,abspath,splitext
import sys
import argparse

sys.path.append(join(dirname(__file__), '..'))
import helper as fn
from mattermost.mattermost_handler import MatterMostHandler as mmhndl

def main(_args):
    """
    check meeting room
        :param params: args
    """

    mm_hndl = mmhndl()
    ret = mm_hndl.delete_message(_args.id)
    if ret:
        print(f"[info] post deleted.")
    else:
        print("[error] no response to update.")
        sys.exit(1)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='check meeting root use ratio.')

    parser.add_argument('id', help='require delete post id')

    args = parser.parse_args()

    main(args)
