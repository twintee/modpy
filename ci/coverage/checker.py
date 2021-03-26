import os
from os.path import isfile, isdir, join, dirname, abspath, splitext
import sys
import json
import argparse

dir_script = abspath(dirname(__file__))

def check_cov(_path, _threshold):
    """
    read coverage json
    """
    if not isfile(_path):
        print(f"[error] not exist cov file: {_path}")
        sys.exit(1)
    with open(_path, 'r', encoding="utf-8") as f:
        cov = json.load(f)
        meta, files, totals = cov["meta"], cov["files"], cov["totals"]
        ret_msg = f"covered [ {float(totals['percent_covered'])} / {float(_threshold)} ]"
        print(f"[info] {ret_msg}")
        if totals["percent_covered"] > float(_threshold):
            print("[info] achieved.")
            return True, ret_msg, meta, files, totals
        else:
            print("[error] not achieved.")
            return False, ret_msg, meta, files, totals
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='gitlab issue tracker charts.')
    parser.add_argument('threshold', help='require fig type "html" or "img"')
    parser.add_argument('cov_path', help='coverage json file path')
    parser.add_argument('--abort', '-a', help='system abort when not achieved', action='store_true')
    args = parser.parse_args()

    ret, msg, meta, files, totals = check_cov(args.cov_path, args.threshold) # pragma: no cover
    if not ret:
        if args.abort:
            sys.exit(1)
