#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
from os.path import join, dirname, isfile, isdir, abspath
import sys
import mattermostdriver as mmdriver
from mattermostdriver import Driver

sys.path.append(join(dirname(__file__), '..'))
import helper as fn

class MatterMost:
    """
    MatterMost

    MatterMost handler class
    *** attention!!!
    if .netrc file exists, read login user setting from .netrc profile

    Attributes:
    ----------
        mat : MatterMostDriver
            mattermost access handler
        team : str
            mattermost url team suffix
        (optional)port : str
            base url to api call
        users : list
            users
    """

    def __init__(self
                 , login_id="", password="", token=""
                 , host="", team="", port=80, verify=False):
        """
        constructor

        Parameters
        -----
        login_id: str
            login id(mail address)
        password: str
            login password(use with login id)
        team: str
            (optional)url suffix
        host: str
            (optional)host name
        port: str
            (optional)host port num
        verify: str
            (optional)host verify
        """

        mm_info = {
            'url': "xx.xx.xx.xx",
            'scheme': 'http',
            'login_id': login_id,
            'password': password,
            'port': port,
            'timeout': 5,
            'verify': verify,
        }

        dir_script = abspath(dirname(__file__))
        path_env = join(dir_script, ".env")

        self.team = "xxxxxxxx"

        if isfile(path_env):
            # envがあれば設定上書き
            print(f"[info] get mminfo from: {path_env}")
            param_env = fn.get_env(path_env)
            login_id = param_env["MM_USER"]
            password = param_env["MM_PASSWORD"]
            host = param_env["MM_HOST"]
            team = param_env["MM_TEAM"]
            port = int(param_env["MM_PORT"])

        if token != "":
            mm_info["token"] = token
        else:
            mm_info["login_id"] = login_id
            mm_info["password"] = password
        if host != "":
            mm_info["url"] = host
        mm_info["port"] = port
        if team != "":
            self.team = team

        self.mat = Driver(mm_info)
        self.mat.login()
        self.users = None
    def logout(self):
        self.mat.logout()

    def get_channel_id(self, ch_name):
        """
        get channel id from api response

        Parameters
        -----
        ch_name : str
            target channel name
        """
        channel_id = self.mat.api['channels'].get_channel_by_name_and_team_name(self.team, ch_name)['id']
        return channel_id

    def get_users(self, opt):
        """
        get user list from api response

        Parameters
        -----
        opt : dict
            filters
        """
        res = self.mat.api['users'].get_users(opt)
        # print(json.dumps(res, indent=2, ensure_ascii=False))
        return res

    def get_user(self, users, match_opt):
        """
        get first match user info from api response

        Parameters
        -----
        users : list
            user list
        match_opt : dict
            filters
        """
        for user in users:
            # print(user)
            for k, v in enumerate(match_opt):
                if user[k] == v:
                    return user
        return None, None, None

    def get_posts(self, ch_name, opt, sort_key=""):
        """
        get posts in channel

        Parameters
        -----
        ch_name : str
            target channel name
        opt : obj
            post filter
        sort_key : str
            sort key field
        """
        try:
            res = self.mat.api['posts'].get_posts_for_channel(
                self.get_channel_id(ch_name)
                , opt
            )
            ret = []
            for p in res['posts'].values():
                ret.append(p)
            if sort_key == "":
                return ret
            else:
                return sorted(ret, key=lambda x:x[sort_key])
        except mmdriver.exceptions.ResourceNotFound as ex:
            return None

    def create_message(self, ch_name, msg):
        """
        post to channel first match user info from api response

        Parameters
        -----
        ch_name : str
            post target channel
        msg : str
            post message
        """
        res = self.mat.api['posts'].create_post(options={
            'channel_id': self.get_channel_id(ch_name),
            'message': msg,
        })
        if "id" in res:
            return res["id"]
        else:
            print(res)
        return None

    def update_message(self, post_id, msg):
        """
        post to channel first match user info from api response

        Parameters
        -----
        post_id : str
            post target id
        msg : str
            update message
        """
        try:
            self.mat.api['posts'].update_post(post_id=post_id, options={
                'id': post_id,
                'message': msg,
            })
        except mmdriver.exceptions.ResourceNotFound as ex:
            return False
        return True

    def delete_message(self, post_id):
        """
        post to channel first match user info from api response

        Parameters
        -----
        post_id : str
            post target id
        msg : str
            update message
        """
        try:
            self.mat.api['posts'].delete_post(post_id=post_id)
        except mmdriver.exceptions.ResourceNotFound as ex:
            return False
        return True
