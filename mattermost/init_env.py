#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
from os.path import isfile,isdir,join,dirname,abspath,splitext
import sys
import argparse

"""
this script make envfile to connect mattermost driver

execute command

python mattermost/init_env.py {scheme} {host} {port} {team} {login_id} {password}

ex.
python mattermost/init_env.py http 11.22.33.44 80 developer aaa@develop.com password

"""

sys.path.append(join(dirname(__file__), '..'))

import helper as fn
from mattermost.mattermost_handler import MatterMostHandler

dir_script = abspath(dirname(__file__))

def main():
    """
    check meeting room
        :param params: args
    """

    MatterMostHandler(_url = args.host,
            _scheme=args.scheme,
            _port=args.port,
            _login_id=args.login_id,
            _password=args.password,
            _team=args.team)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='check meeting root use ratio.')

    parser.add_argument('scheme', help='mattermost host scheme', default='http')
    parser.add_argument('host', help='mattermost host address without scheme. (xx.xx.xx.xx or xxx.yyy.com)')
    parser.add_argument('port', help='mattermost port number')
    parser.add_argument('team', help='mattermost team directive')
    parser.add_argument('login_id', help='mattermost user mail address.')
    parser.add_argument('password', help='mattermost user password')

    args = parser.parse_args()
    path_env = join(dir_script, ".env")

    main()
