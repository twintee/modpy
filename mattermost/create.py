#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
from os.path import isfile, isdir, join, dirname, abspath, splitext
import sys
import argparse

sys.path.append(join(dirname(__file__), '..'))

from mattermost.mattermost_handler import MatterMostHandler as mmhndl

def main(_args):
    """
    check meeting room
        :param params: args
    """
    mm_hndl = mmhndl()
    res_id = mm_hndl.create_message(_args.ch_name, _args.msg)
    if res_id is None:
        print("[error] not response post id.")
        sys.exit(1)
    else:
        print(f"[info] posted to mattermost. [{res_id}]")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='check meeting root use ratio.')

    # parser.add_argument('user', help='require mail address or username')
    # parser.add_argument('passwd', help='require password for post user')
    parser.add_argument('ch_name', help='post channel name')
    parser.add_argument('msg', help='post message')

    args = parser.parse_args()

    main(args)
