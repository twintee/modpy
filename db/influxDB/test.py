#!/usr/bin/python
# -*- coding: utf-8 -*-
"""influxDB helper

Usage
-----
    * install influxdb
    `pip3 install influxdb`
    * execute test.py

"""
import os
import sys
import json
import argparse
import time
from dotenv import load_dotenv
from influxdb.resultset import ResultSet as ifret

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
import helper as fn
from db.influxDB.ifmod import influxClient

dir_script = os.path.abspath(os.path.dirname(__file__))
os.chdir(dir_script)
file_env = os.path.join(dir_script, ".env")

def get_env(_ref, _keys):
    """
    make .env file
    """
    load_dotenv(_ref)
    env_data = {}

    for i, key in enumerate(_keys):
        env_data[key] = os.getenv(key)
    return env_data

def write_env(_params):
    """
    make .env file
    """
    lines = ""
    for key, val in _params.items():
        lines += f"{key}={val}\n"
    # ファイル名保存
    with open(file_env, mode="w", encoding="utf8") as f:
        f.write(lines)

def insert_data(_fields, _tags):
    """
    add new record
    """
    if_hndl.write_points(meas, _fields, _tags)

def update_data(_time, _fields, _tags):
    """
    update record
    """
    _fields["time"] = _time
    if_hndl.write_points(meas, _fields, _tags)

def get_data(_fields=[]):
    fields = "*"
    if len(_fields) > 0:
        print(len(_fields))
        fields = ",".join(_fields)
    query = f"SELECT {fields} FROM {meas} ORDER by time asc"
    ret = if_hndl.get_points(query)
    return list(ret)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='check meeting root use ratio.')
    parser.add_argument('cmd', help='require node type "master" or "worker" or "build"')
    parser.add_argument('-r', "--reset", help='(option) reset influxDB host params', action='store_true')
    args = parser.parse_args()

    if not args.cmd in ["insert", "get", "update"]:
        print("[error] args error.")
        sys.exit()
    if_keys = [
            "IF_HOST",
            "IF_PORT",
            "IF_USER",
            "IF_PASSWORD",
            "IF_DATABASE",
            "IF_MEASUREMENT",
        ]
    if not os.path.isfile(file_env) or args.reset:
        params = fn.input_params(if_keys)
        write_env(params)
    if_host = get_env(file_env, if_keys)

    if_hndl = influxClient(
        if_host["IF_HOST"],
        if_host["IF_USER"],
        if_host["IF_PASSWORD"],
        if_host["IF_DATABASE"],
        int(if_host["IF_PORT"])
        )
    meas = if_host["IF_MEASUREMENT"]

    field_keys = [
        "estimate",
        "data2",
        "data3",
    ]
    tag_keys = [
        "sprint",
        "week",
    ]

    if args.cmd == "insert":
        fields = {
            "estimate": 100,
            "data2": 200,
            "data3": 300,
            }
        tags = {
            "sprint": "sprint30",
            "week": 10,
            }
        insert_data(fields, tags)
    if args.cmd == "get":
        ret = get_data()
        for recs in ret:
            for rec in recs:
                print(rec)
    if args.cmd == "update":
        get_rec = get_data()
        for recs in get_rec:
            for rec in recs:
                print(rec)
                fields = {
                    "estimate": 500,
                    }
                tags = {
                    "week": 20,
                    }
                update_data(rec["time"], fields, tags)
    print("----------initialize end.")
