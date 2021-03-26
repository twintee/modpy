#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
from os.path import isfile, isdir, join, dirname, abspath, splitext
import sys
from mattermostdriver import Driver as mmDriver, exceptions as mmex

sys.path.append(join(dirname(__file__), '..'))
from loader.env_loader import EnvLoader

class MatterMostHandler:
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

    def __init__(self,
            _url:str=None,
            _scheme:str='http',
            _port:int=None,
            _login_id:str=None,
            _password:str=None,
            _token:str=None,
            _team:str=None,
            _verify:bool=False,
            _envfile:str=".env"):
        """
        constructor

        Parameters
        -----
        url: str
            (optional)host name
        scheme: str
            (optional)host name
        port: str
            (optional)host port num
        login_id: str
            login id(mail address)
        password: str
            login password(use with login id)
        team: str
            (optional)url suffix
        verify: str
            (optional)host verify
        """

        self.mminfo = {
            'scheme': _scheme,
            'port': _port,
        }

        dir_script = abspath(dirname(__file__))
        path_env = join(dir_script, _envfile)

        # envがあれば初期値読み込み
        self.env = EnvLoader(path_env)
        if isfile(path_env):
            print(f"[info] get mminfo from: {path_env}")
            self.mminfo["url"] = self.env.get("url")
            self.mminfo["port"] = self.env.get("port")
            self.mminfo["login_id"] = self.env.get("login_id")
            self.mminfo["password"] = self.env.get("password")
            # self.mminfo["token"] = self.env.get("token")
            self.mminfo["team"] = self.env.get("team")

        # 引数上書き
        if not _url is None:
            self.mminfo["url"] = _url
        if not _port is None:
            self.mminfo["port"] = _port
        if not _login_id is None:
            self.mminfo["login_id"] = _login_id
        if not _password is None:
            self.mminfo["password"] = _password
        # if not _token is None:
        #     self.mminfo["token"] = _token
        #     if "login_id" in self.mminfo:
        #         del self.mminfo["login_id"], self.mminfo["password"]
        #     if "password" in self.mminfo:
        #         del self.mminfo["password"]
        # else:
        #     self.mminfo["login_id"] = _login_id
        #     self.mminfo["password"] = _password
        #     if "token" in self.mminfo:
        #         del self.mminfo["token"]
        if not _team is None:
            self.mminfo['team'] = _team

        self.hndl = mmDriver({
                'url': self.mminfo['url'],
                'scheme': self.mminfo['scheme'],
                'login_id': self.mminfo['login_id'],
                'password': self.mminfo['password'],
                'port': int(self.mminfo['port']),
                'timeout': 5,
                'verify': _verify,
                })
        self.hndl.login()

        self.env.save(_params=self.mminfo)
        self.users = None
    def logout(self):
        self.hndl.logout()

    def get_channel_id(self, ch_name):
        """
        get channel id from api response

        Parameters
        -----
        ch_name : str
            target channel name
        """
        channel_id = self.hndl.api['channels'].get_channel_by_name_and_team_name(self.mminfo['team'], ch_name)['id']
        return channel_id

    def get_users(self, opt):
        """
        get user list from api response

        Parameters
        -----
        opt : dict
            filters
        """
        res = self.hndl.api['users'].get_users(opt)
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
            res = self.hndl.api['posts'].get_posts_for_channel(
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
        except mmex.ResourceNotFound as ex:
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
        res = self.hndl.api['posts'].create_post(options={
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
            self.hndl.api['posts'].update_post(post_id=post_id, options={
                'id': post_id,
                'message': msg,
            })
        except mmex.ResourceNotFound as ex:
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
            self.hndl.api['posts'].delete_post(post_id=post_id)
        except mmex.ResourceNotFound as ex:
            return False
        return True
