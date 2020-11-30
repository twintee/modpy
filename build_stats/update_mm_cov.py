#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import helper as fn
from mattermost.mm import MatterMost

from ci.coverage.checker import check_cov

def main(_args):
    """
    check meeting room
        :param params: args
    """

    ret, msg, meta, files, totals = check_cov(cov_path, _args.threshold)

    stat_path = os.path.join(path_cwd, os.path.dirname(__file__), _args.stat_path)
    if fn.check_path("update_mm_stat", stat_path):
        stat_json = fn.load_json(stat_path)

        result = "success" if ret else "fail"
        if "results" not in stat_json:
            stat_json["results"] = {}
        stat_json["results"][_args.stage] = result
        stat_json[_args.stage] = f"""**[ {result} ]**
  * {msg}"""

        post_msg = f"***\n【STATUS】\n[{_args.stage}] - {_args.msg} [{result}]\n***"
        for k, stat in stat_json.items():
            if k != "mm_id" and k != "results":
                post_msg += f"\n* {k} : {stat}"
        print(f"{stat_json['mm_id']}, {post_msg}")
        mm_hndl.update_message(stat_json["mm_id"], post_msg)

        fn.save_json(stat_path, stat_json)
    else:
        print(f"[error] not exist stat file. [{stat_path}]")
        sys.exit(1)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='check meeting root use ratio.')

    parser.add_argument('ch_name', help='require post channel name')
    parser.add_argument('stage', help='require process stage name')
    parser.add_argument('msg', help='require post message')
    parser.add_argument('stat_path', help='require relational path to save stat json')

    parser.add_argument('cov_path', help='require relational json path')
    parser.add_argument('threshold', help='coverage threshold')

    args = parser.parse_args()

    mm_hndl = MatterMost()
    path_cwd = os.getcwd()
    cov_path = os.path.join(path_cwd, os.path.dirname(__file__), "..", "..", args.cov_path)

    main(args)
