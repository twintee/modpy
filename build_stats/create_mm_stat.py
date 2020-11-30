#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import helper as fn
from mattermost.mm import MatterMost

dir_script = os.path.abspath(os.path.dirname(__file__))

def main(_args):
    """
    check meeting room
        :param params: args
    """
    path_cwd = os.getcwd()
    mm_hndl = MatterMost()
    post_msg = _args.msg

    res_id = mm_hndl.create_message(_args.ch_name, post_msg)
    if not res_id is None:
        stat_path = os.path.join(path_cwd, os.path.dirname(__file__), _args.stat_path)
        stat_json = {
            "mm_id": f"{res_id}"
            }
        stat_json[_args.stage] = _args.stat_value
        fn.save_json(stat_path, stat_json)
        post_msg = f"***\n【STATUS】\n[{_args.stage}] : {_args.msg}\n***"
        for k, stat in stat_json.items():
            if k != "mm_id" and k!= "results":
                post_msg += f"\n* {k} : {stat}"
        mm_hndl.update_message(res_id, post_msg)
    else:
        print("[error] not response post id.")
        sys.exit(1)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='check meeting root use ratio.')

    parser.add_argument('ch_name', help='require post channel name')
    parser.add_argument('stage', help='require process stage name')
    parser.add_argument('msg', help='require post message')
    parser.add_argument('stat_path', help='relational path to save stat json')
    parser.add_argument('stat_value', help='update value to save stat json')

    args = parser.parse_args()

    main(args)
