#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import requests

req_info = {
    'url': "http://xx.xx.xx.xx:xxxx/xxxxxxxx",
    'user': "xxx",
    'user_token': 'xxxxxxxxx',
}

def get_crumb():
    """
    get crumb to access jenkins api

    Returns
    ----------
    crumb : string
        jenkins crumb
    """

    req_url = f"{req_info['url']}/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,\":\",//crumb)"
    req_auth = (req_info['user'], req_info['user_token'])

    response = requests.get(req_url, auth=req_auth)
    spl = response.content.decode().split(":")
    print(f"get_crumb: {spl[1]}")
    return spl[1]

def req_build(job_name):
    """
    send build request to jenkins server

    Parameters
    -----
    job_name : str
        request job name.

    Returns
    ----------
    result : bool
    """
    ret_crumb = get_crumb()
    req_header = {
        'Content-Type': 'application/json',
        'Jenkins-Crumb': ret_crumb,
    }
    req_url = f"{req_info['url']}/job/{job_name}/build"
    print(req_url)
    req_auth = (req_info['user'], req_info['user_token'])

    response = requests.post(req_url
                             , auth=req_auth
                             , headers=req_header)
    print(response)
    return True

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='check meeting root use ratio.')

    parser.add_argument('job_name', help='require build job name.')

    args = parser.parse_args()

    req_build(args.job_name)

