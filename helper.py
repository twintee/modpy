#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import json
import time
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

def get_env(_path):
    """
    update env param
    """
    if not os.path.isfile(_path):
        print(f"[info] not exist env file. {_path}")
        return {}

    # ファイル行読みしながらテキスト置き換え
    with open(_path, 'r', encoding="utf8") as f:
        ret = {}
        while True:
            line = f.readline()
            if line:
                spl = line.replace('\n', '').split("=", 2)
                ret[spl[0]] = spl[1]
            else:
                break
        return ret

def set_env(_path, _params, _reset=False):
    """
    update env param
    """

    if not _reset:
        m_params = get_env(_path)
        _params.update(m_params)
    new_lines = ""
    for k, v in _params.items():
        new_lines += f"{k}={v}\n"
    # ファイル名保存
    with open(_path, mode="w", encoding="utf8") as f:
        f.write(new_lines)

def elapse_timer(_ref_frame, _pre="", _suf=""):
    """
    処理時間計測用。基準時間からcallされた時間までの差分時間を表示。

    Parameters
    ----------
    - ref_frame : float
        差分の基準時間
    - pref : str
        表示テキストのプレフィックス
    - suff : str
        表示テキストのサフィックス

    Returns
    -------
    - get_frame : float
        差分計測用に取得した時間
    """
    get_frame = time.time()
    elapsed_frame = get_frame - _ref_frame
    print(f"{_pre}{elapsed_frame}{_suf}")
    return get_frame

def check_path(_cls: str, _ref: str, _abort=False):
    """
    パスの存在確認

    Parameters
    -----
    _cls : str
        参照元。
    _ref : str
        確認するパス
    _abort : bool
        存在しない場合処理中断するか。

    Returns
    -----
    - result:bool
    """
    if not os.path.exists(_ref):
        print(f'[error] {_cls}: not exist file. [{_ref}]')
        if _abort:
            sys.exit()
        return False
    return True

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

def load_json(_ref: str):
    """
    read json file

    Parameters
    ----------
    _ref : str
        open json file path
    """

    check_path(sys._getframe().f_code.co_name, _ref)
    with open(_ref, 'r', encoding="utf-8") as f:
        return json.load(f)

def save_json(_dist: str, _settings):
    """
    save json file

    Parameters
    ----------
    _dist : str
        save json file path
    _settings : dict
        save target dict
    """
    with open(_dist, "w", encoding="utf-8") as dist:
        json.dump(_settings, dist, indent=4, ensure_ascii=False)

def load_setting(_ref: str, _dist: str, _settings, _sep="@"):
    """
    replace text enclosed '@' by _settings include key and values

    Parameters
    ----------
    _ref : str
        original file
    _dist : str
        output path
    _settings : dict
        reference replace setting json
    _sep : str
        sand str for replace word(default "@")
    """

    check_path(sys._getframe().f_code.co_name, _ref)

    with open(_ref, 'r', encoding="utf-8") as ref:
        data_ref = ref.read()
    for k, val in _settings.items():
        data_ref = data_ref.replace(f"{_sep}{k}{_sep}", f"{val}")

    with open(_dist, "w", encoding="utf-8") as dist:
        dist.write(data_ref)

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


def find_text(_ref, _find):
    """
    check word in text file

    Parameters
    -----
    _ref: str
        target path
    _find: str
        search word
    """
    check_path(sys._getframe().f_code.co_name, _ref)
    with open(_ref) as flines:
        for row, text in enumerate(flines, start=1):
            text = text.rstrip()
            if _find in text:
                return True
    return False

def ymd_to_timestamp(ymd, is_ms=False):
    """
    yyyymmddhhiiss convert to timestamp

    Parameters
    -----
    _ymd : str
        target date str
    _is_ms : str
        comvert to ms style
    """
    ret = dt.strptime(ymd, '%Y/%m/%d %H:%M:%S').timestamp()
    if is_ms:
        ret = f"{int(ret)}000"
    return int(ret)

