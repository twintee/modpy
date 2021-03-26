#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
from os.path import isfile
import sys
from datetime import datetime as dt
import string
import random
import subprocess
import socket

def input_params(_keys):
    """
    update env param
    """
    ret = {}
    for i,key in enumerate(_keys):
        _input = input(f"input {key} value. :")
        ret[key] = _input
    return ret

def get_local_ip():
    """
    socketを使ってローカルIPを取得

    Returns
    ----------
    get_ip : str
        取得したIPアドレス
    """
    get_ip = [
        (s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]
        ][0][1]
    return get_ip

def random_str(_n: int):
    """
    generate random text include number and alphabets

    Parameters
    -----
    _n : int
        generate text length
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=_n))

def cmd_lines(_cmd, _cwd="", _encode='cp932', _wait_enter=False):
    """
    execute command and stream text

    Parameters
    -----
    _cmd : list or str
        commands list
    _cwd : str
        current work dir.
    _encode : str
        default value cp932 (set utf-8 fix errors)
    """
    if isinstance(_cmd, list):
        for ref in _cmd:
            print(f"\n[info] command executed. [{ref}]")
            if _wait_enter:
                input("enter to execute cmd. ([ctrl + c] to cancel script)")
            cmd = ref.split()
            if _cwd == "":
                proc = subprocess.Popen(cmd
                                        , stdout=subprocess.PIPE
                                        , stderr=subprocess.STDOUT
                                        , shell=True)
            else:
                proc = subprocess.Popen(cmd
                                        , cwd=_cwd
                                        , stdout=subprocess.PIPE
                                        , stderr=subprocess.STDOUT
                                        , shell=True)
            while True:
                line = proc.stdout.readline()
                if line:
                    yield line.decode(_encode)
                if not line and proc.poll() is not None:
                    break
    else:
        print(f"\n[info] command executed. [{_cmd}]")
        if _wait_enter:
            input("enter to execute cmd. ([ctrl + c] to cancel script)")
        cmd = _cmd.split()
        if _cwd == "":
            proc = subprocess.Popen(cmd
                                    , stdout=subprocess.PIPE
                                    , stderr=subprocess.STDOUT)
        else:
            proc = subprocess.Popen(cmd
                                    , cwd=_cwd
                                    , stdout=subprocess.PIPE
                                    , stderr=subprocess.STDOUT)
        while True:
            line = proc.stdout.readline()
            if line:
                yield line.decode(_encode)
            if not line and proc.poll() is not None:
                break

def find_text(_ref, _find, _first=True):
    """
    check word in text file

    Parameters
    -----
    _ref: str
        target path
    _find: str
        search word
    """
    ret = None
    if not isfile(_ref):
        print(f"[error] no file: {_ref}")
        return None
    with open(_ref) as flines:
        for i, text in enumerate(flines, start=1):
            text = text.rstrip()
            if _find in text:
                if _first:
                    return text
                if ret is None:
                    ret = []
                ret.append(text)
    return ret

def timestr_to_timestamp(_ref_time=None, _is_ms=False):
    """
    yyyymmddhhiiss convert to timestamp

    Parameters
    -----
    _ymd : str
        target date str
    _is_ms : str
        comvert to ms style
    """
    if _ref_time is None:
        _ref_time = dt.now().strftime('%Y%m%d%H%M%S')
    ret = dt.strptime(_ref_time, '%Y/%m/%d %H:%M:%S').timestamp()
    if _is_ms:
        ret = f"{int(ret)}000"
    return int(ret)

