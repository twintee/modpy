#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import helper as fn

dir_script = os.path.abspath(os.path.dirname(__file__))

def main(_args):
    """
    check meeting room
        :param params: args
    """
    params = {}
    if not _args.user is None:
        params["MM_USER"] = _args.user
    if not _args.passwd is None:
        params["MM_PASSWORD"] = _args.passwd
    if not _args.host is None:
        params["MM_HOST"] = _args.host
    if not _args.team is None:
        params["MM_TEAM"] = _args.team
    if not _args.port is None:
        params["MM_PORT"] = _args.port

    fn.set_env(path_env, params)

    print(fn.get_env(path_env))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='check meeting root use ratio.')

    parser.add_argument('user', help='mattermost user')
    parser.add_argument('passwd', help='mattermost login password')
    parser.add_argument('host', help='mattermost host address')
    parser.add_argument('team', help='mattermost team directive')
    parser.add_argument('port', help='mattermost port number')

    args = parser.parse_args()
    path_env = os.path.join(dir_script, ".env")

    main(args)
