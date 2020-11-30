#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import helper as fn
from mattermost.mm import MatterMost

def main(_args):
    """
    check meeting room
        :param params: args
    """

    mm_hndl = MatterMost()
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
