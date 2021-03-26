#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
from os.path import isfile,isdir,join,dirname,abspath,splitext
import sys
import argparse

"""
this script make envfile to connect influxDB

execute command

python db/influxDB/init_env.py {scheme} {host} {port} {team} {login_id} {password}

ex.
python mattermost/init_env.py http 11.22.33.44 80 developer aaa@develop.com password

"""

sys.path.append(join(dirname(__file__), '..'))
from db.influxDB.influxdb_handler import InfluxDbHandler

dir_script = abspath(dirname(__file__))

def main():
    """
    check meeting room
        :param params: args
    """

    InfluxDbHandler(_host = args.host,
            _user=args.login_id,
            _passwd=args.password,
            _db=args.db,
            _port=args.port)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='init envfile for connecting influxDB.')

    parser.add_argument('host', help='influxdb host address. (http://xx.xx.xx.xx)')
    parser.add_argument('port', help='influxdb port number')
    parser.add_argument('login_id', help='influxdb user id.')
    parser.add_argument('password', help='influxdb user password')
    parser.add_argument('db', help='influxdb database name')

    args = parser.parse_args()
    path_env = join(dir_script, ".env")

    main()
