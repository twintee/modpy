#!/usr/bin/python
# -*- coding: utf-8 -*-
"""influxDB helper

Usage
-----
    * install influxdb
    `pip3 install influxdb`

"""
import os
from os.path import isfile, isdir, join, dirname, abspath, splitext
import sys
import json
from datetime import datetime as dt
import argparse

sys.path.append(abspath(join(dirname(__file__), '..', '..')))
from db.influxDB.influxdb_handler import InfluxDbHandler

dir_script = abspath(dirname(__file__))
os.chdir(dir_script)
file_env = join(dir_script, ".env")

def get_data():

    fields = "*"
    if not args.fields is None:
        if len(args.fields) > 0:
            fields = ",".join(args.fields)
    qwhere = ""
    if not args.time is None:
        if qwhere != '':
            qwhere = ' AND '
        qwhere += f"time {format_time(args.time)}"
    if not args.tags is None:
        for tag, val in json.loads(args.tags):
            if qwhere != '':
                qwhere = ' AND '
            qwhere += f'"{tag}"="{val}"'
    qgroup = ""
    if not args.groupby is None:
        qgroup += f"{(args.groupby)}"
    qlimit = ""
    if not args.limit is None:
        qlimit += f"{(args.limit)}"
    qtimezone = ""
    if not args.timezone is None:
        qtimezone = f'tz("{args.timezone}"")'

    query = f"SELECT {fields} FROM {args.meas} ORDER by time asc"
    if qwhere != "":
        query += f" WHERE {qwhere}"
    if qgroup != "":
        query += f" GROUP BY {qgroup}"
    if qlimit != "":
        query += f" LIMIT {qlimit}"
    if qtimezone != "":
        query += f" {qtimezone}"
    query += f" ORDER by time asc"

    ifhndl = InfluxDbHandler()
    ret = ifhndl.get_points(query)

    return list(ret)

def format_time(_time):
    if len(_time) == 14:
        return f"{_time[:4]}-{_time[4:6]}-{_time[6:8]}T{_time[8:10]}:{_time[10:12]}:{_time[12:]}Z"
    else:
        return f"{_time[:4]}-{_time[4:6]}-{_time[6:8]}T{_time[8:10]}:{_time[10:12]}:{_time[12:14]}.{_time[14:]}Z"

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='check meeting root use ratio.')
    parser.add_argument('meas', help='insert measurement name')
    parser.add_argument('fields', help='insert value. ex. field1,field2...MEAN(field1),SUM(field2) ', type=str)
    parser.add_argument('--tags', help='where tags dict.', type=str)
    parser.add_argument('--limit', '-l', help='limit result num', type=str)
    parser.add_argument('--time', '-t', help="where time from query. ex. '20200501235959000000'", type=str)
    parser.add_argument('--timezone', help="where timezone. ex. 'Asia/Tokyo'", type=str)
    parser.add_argument('--groupby', '-g', help='groupby query format. ex. time(6h)', type=str)
    args = parser.parse_args()

    if not args.time is None:
        if len(args.time) < 14:
            print("[error] args: time length error.")

    get_data()
    print("---------- end.")
