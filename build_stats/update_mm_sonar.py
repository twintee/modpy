#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import helper as fn
from mattermost.mm import MatterMost

from ci.sonarqube.checker import check_sonar_issue, check_sonar_metric

def main(_args):
    """
    check meeting room
        :param params: args
    """

    ret_issue, msg_issue = check_sonar_issue(args.sn_url, args.sn_user, args.sn_passwd, args.sn_project_key)
    ret_dupe, msg_dupe = check_sonar_metric(args.sn_url, args.sn_user, args.sn_passwd, args.sn_project_key, "duplicated_lines")
    ret_bug, msg_bug = check_sonar_metric(args.sn_url, args.sn_user, args.sn_passwd, args.sn_project_key, "bugs")

    stat_path = os.path.join(path_cwd, os.path.dirname(__file__), _args.stat_path)
    if fn.check_path("update_mm_stat", stat_path):
        stat_json = fn.load_json(stat_path)

        result = "success" if ret_issue and ret_dupe and ret_bug else "fail"
        if "results" not in stat_json:
            stat_json["results"] = {}
        stat_json["results"][_args.stage] = result
        stat_json[_args.stage] = f"""**[ {result} ]**
| category | result | report |
| --- | :---: | --- |
| issues | **{"success" if ret_issue else "fail"}** | {msg_issue} |
| duplicated_lines | **{"success" if ret_dupe else "fail"}** | {msg_dupe} |
| bugs | **{"success" if ret_bug else "fail"}** | {msg_bug} |"""

        post_msg = f"""***
【STATUS】
[{_args.stage}] - {_args.msg} [{result}]
check report. [sonarqube]({_args.sn_url}/dashboard/index/{_args.sn_project_key}
***"""
        for k, stat in stat_json.items():
            if k != "mm_id" and k != "results":
                post_msg += f"\n* **{k}** : {stat}"
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

    parser.add_argument('sn_url', help='require sonar url')
    parser.add_argument('sn_user', help='require sonar username')
    parser.add_argument('sn_passwd', help='require sonar passwd')
    parser.add_argument('sn_project_key', help='require sonar project key')


    args = parser.parse_args()

    mm_hndl = MatterMost()
    path_cwd = os.getcwd()

    main(args)
