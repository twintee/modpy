#!/usr/bin/python
# -*- coding: utf-8 -*-
"""influxDB helper

insert point

ex.
python db/influxDB/insert.py meas "{\"f\":\"1\", \"ff\":2}" "{\"t1\":3}" -t 20210326111111

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

def insert_data():
    """
    add new record
    """
    json_data = get_format_data()
    print(json_data)
    ifhndl = InfluxDbHandler()
    ifhndl.write_points(json_data)

def get_format_data():

    ret = {
            "fields": json.loads(args.fields),
            "tags": json.loads(args.tags),
            "measurement": args.meas,
            }
    if not args.time is None:
        ret['time'] = format_time(args.time)
    if args.now:
        ret['time'] = dt.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    return [ret]

def format_time(_time):
    if len(_time) == 14:
        return f"{_time[:4]}-{_time[4:6]}-{_time[6:8]}T{_time[8:10]}:{_time[10:12]}:{_time[12:]}Z"
    else:
        return f"{_time[:4]}-{_time[4:6]}-{_time[6:8]}T{_time[8:10]}:{_time[10:12]}:{_time[12:14]}.{_time[14:]}Z"

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='check meeting root use ratio.')
    parser.add_argument('meas', help='insert measurement name')
    parser.add_argument('fields', help='insert fields.', type=str)
    parser.add_argument('tags', help='point tags.', type=str)
    parser.add_argument('--time', '-t', help='time format like yyyyMMddhhiiss', type=str)
    parser.add_argument('--now', '-n', help='get now time format like yyyyMMddhhiiss', action='store_true')
    args = parser.parse_args()

    if not args.time is None:
        if len(args.time) < 14:
            print("[error] args: time length error.")

    insert_data()
    print("---------- end.")
