#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
from os.path import isfile, isdir, join, dirname, abspath, splitext
import requests
import argparse

dir_script = abspath(dirname(__file__))

def check_sonar_issue(_host, _user, _pass, _project_key, _severities=None, _statuses=None):
    """
    get sonarqube issues from sonar API

    ---

    Parameters
    _host: str
        sonar host address
    _user: str
        sonar user username
    _pass: str
        sonar user password
    _project_key: str
        sonar project key
    _severities: list
    _statuses: list
    """

    severities = "BLOCKER,CRITICAL,MAJOR,MINOR"
    if not _severities is None:
        severities = ",".join(_severities)
    statuses = "OPEN,REOPENED"
    if not _statuses is None:
        statuses = ",".join(_statuses)
    req_url = f"{_host}/api/issues/search?componentRoots={_project_key}&severities={severities}&statuses={statuses}"
    sonar_url = f"{_host}/project/issues?id={_project_key}&resolved=false"
    ret = requests.get(req_url)
    result = True
    msg = "sonarqube static analytics issues: OK"
    if ret.status_code != 200:
        msg = f"sonarqube request failed. status code: [{ret.status_code}]"
        result = False
    else:
        ret_json = ret.json()
        if "issues" not in ret_json:
            msg = "not exist issue data."
            result = False
        else:
            if ret_json["total"] > 0:
                msg = f"sonar issues exists. check [sonar report]({sonar_url})"
                result = False
    if result:
        print(f"[info] {msg}")
    else:
        print(f"[error] {msg}")
    return result, msg

def check_sonar_metric(_host, _user, _pass, _project_key, _metric_key):
    """
    get sonarqube duplications from sonar API

    ---

    Parameters
    _host: str
        sonar host address
    _user: str
        sonar user username
    _pass: str
        sonar user password
    _project_key: str
        sonar project key
    _severities: list
    _statuses: list
    """

    req_url = f"{_host}/api/measures/component?component={_project_key}&metricKeys={_metric_key}"
    sonar_url = f"{_host}/component_measures?id={_project_key}&metric={_metric_key}"
    ret = requests.get(req_url)
    result = True
    msg = f"sonarqube static analytics {_metric_key}: OK"
    if ret.status_code != 200:
        msg = f"sonarqube request failed. status code: [{ret.status_code}]"
        result = False
    else:
        ret_json = ret.json()
        for k, meas in enumerate(ret_json["component"]["measures"]):
            if meas["metric"] == _metric_key:
                if float(meas["value"]) > 0:
                    msg = f"sonar metric[{_metric_key}] exists. check [sonar report]({sonar_url})"
                    result = False
                break
    if result:
        print(f"[info] {msg}")
    else:
        print(f"[error] {msg}")
    return result, msg

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='gitlab issue tracker charts.')
    parser.add_argument('host', help='require sonar hostname')
    parser.add_argument('user', help='require sonar username')
    parser.add_argument('passwd', help='require sonar passwd')
    parser.add_argument('project_key', help='require sonar project key')
    parser.add_argument('--abort', '-a', help='system abort when not achieved', action='store_true')
    args = parser.parse_args()

    # ret, msg = check_sonar_issue(args.host, args.user, args.passwd, args.project_key)
    ret, msg = check_sonar_metric(args.host, args.user, args.passwd, args.project_key, "duplicated_lines")
    # ret, msg = check_sonar_metric(args.host, args.user, args.passwd, args.project_key, "bugs")
    # if not ret:
    #     if args.abort:
    #         sys.exit(1)
