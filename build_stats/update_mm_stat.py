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
    stat_path = os.path.join(path_cwd, os.path.dirname(__file__), _args.stat_path)
    if fn.check_path("update_mm_stat", stat_path):
        stat_json = fn.load_json(stat_path)

        stat_json[_args.stage] = _args.stat_value

        # 現状
        post_msg = f"""***
【STATUS】
[{_args.stage}] - {_args.msg}
***"""
        # 全体
        for k, stat in stat_json.items():
            if k != "mm_id" and k != "results":
                post_msg += f"\n* {k} : {stat}"

        print(f"{stat_json['mm_id']}, {post_msg}")
        mm_hndl.update_message(stat_json["mm_id"], post_msg)
        fn.save_json(stat_path, stat_json)
    else:
        print(f"[error] not exist stat_file. [{stat_path}]")
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
