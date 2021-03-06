#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
from os.path import isfile, basename
import sys
from datetime import datetime as dt
import string
import random
import subprocess
import socket

def input_yn(_txt, _yes=False):
    if _yes:
        print(f"{_txt}y")
        return True
    _input = input(_txt).lower()
    if _input in ["y", "yes"]:
        return True
    return False

def input_list(_message, _list):
    req_num = -1
    def print_list():
        print(f"\n-------------------------------\n{_message}")
        for i, filter in enumerate(_list):
            print(f"[{i + 1}] {basename(filter)}")
    while req_num < 0 or req_num >= len(_list):
        print_list()
        _input = input("\ninput number. :")
        if _input != "":
            req_num = int(_input) - 1
        if req_num < 0 or req_num >= len(_list):
            print("\n[error] input number error.")
    return req_num

def info(message, time=True):
    print_message(message, time=time)

def error(message, time=True):
    print_message(message, error=True, time=time)

def print_message(message, error=False, time=True):
    """
    メッセージ表示
    """
    text = "[info]"
    if error:
        text = "[error]"
    if time:
        text += f" {dt.now().strftime('%Y-%m-%d %H:%M:%S')}"
    print(f"{text}")

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

def cmdlines(_cmd, _cwd="", _encode='cp932', _wait_enter=False, _no_split=False):
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
            if _no_split:
                cmd = ref
            if _cwd == "":
                proc = subprocess.Popen(cmd
                                        , stdout=subprocess.PIPE
                                        , stderr=subprocess.STDOUT
                                        , shell=_no_split)
            else:
                proc = subprocess.Popen(cmd
                                        , cwd=_cwd
                                        , stdout=subprocess.PIPE
                                        , stderr=subprocess.STDOUT
                                        , shell=_no_split)
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
        if _no_split:
            cmd = _cmd
        if _cwd == "":
            proc = subprocess.Popen(cmd
                                    , stdout=subprocess.PIPE
                                    , stderr=subprocess.STDOUT
                                    , shell=_no_split)
        else:
            proc = subprocess.Popen(cmd
                                    , cwd=_cwd
                                    , stdout=subprocess.PIPE
                                    , stderr=subprocess.STDOUT
                                    , shell=_no_split)
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

def get_timestamp(_ref_time=None):
    """
    yyyymmddhhiiss convert to timestamp

    Parameters
    -----
    _ymd : str
        formatted string YYYY/mm/dd HH:MM:SS.ffffff
        no arg to get now timestamp
    """
    if _ref_time is None:
        return dt.now().timestamp()
    try:
        if len(_ref_time) > 19:
            return dt.strptime(_ref_time, '%Y/%m/%d %H:%M:%S.%f').timestamp()
        elif len(_ref_time) == 19:
            return dt.strptime(_ref_time, '%Y/%m/%d %H:%M:%S.%f').timestamp()
        else:
            return None
    except ValueError as e:
        print(e)
    return None

