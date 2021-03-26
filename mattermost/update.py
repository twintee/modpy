#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
from os.path import isfile, isdir, join, dirname, abspath, splitext
import sys
import argparse

sys.path.append(join(dirname(__file__), '..'))
from mattermost.mm import MatterMostHandler as mmhndl

def main(_args):
    """
    check meeting room
        :param params: args
    """

    mm_hndl = mmhndl(_login_id=_args.user, _password=_args.passwd)
    ret = mm_hndl.update_message(_args.id, _args.msg)
    if ret:
        print(f"[info] post updated.")
    else:
        print("[error] no response to update.")
        sys.exit(1)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='check meeting root use ratio.')

    parser.add_argument('user', help='require mail address or username')
    parser.add_argument('passwd', help='require password for post user')
    parser.add_argument('id', help='require update post id')
    parser.add_argument('msg', help='require post message')

    args = parser.parse_args()

    main(args)
