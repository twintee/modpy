#! /usr/bin/env python
# -*- coding: utf-8 -*-
import requests

class GitLab:
    """GitLab Api handler class

    Attributes:
    ----------
        url : str
            api base url
        token : str
            gitbucket user token
        req_header : str
            api request header
    """

    def __init__(self, _url="", _token=""):
        """
        constructor

        Parameters
        -----
        _url : str
            host name
        _token : str
            user token
        """

        self.url = "http://xxxxxxxx/api/v4"
        if _url != "":
            self.url = _url

        self.token = "xxxxxxxx"
        if _token != "":
            self.token = _token

        self.req_header = {'Private-Token' : f"{self.token}"}

    def get(self, _ext_url):
        """
        get project info

        Returns
        -----
        ret : dict
            api response json object
        """
        req_url = f"{self.url}/{_ext_url}"
        ret = requests.get(req_url, headers = self.req_header)
        return ret.json()

    def get_projects(self, _is_simple=False):
        """
        get project info

        Returns
        -----
        ret : dict
            api response json object
        """
        req_url = f"{self.url}/projects"
        if _is_simple:
            req_url += "?simple=true"
        ret = requests.get(req_url, headers = self.req_header)
        return ret.json()

    def get_project_info(self, _group, _prj_name):
        """
        get project info

        Parameters
        -----
        prj_name : str
            search project name

        Returns
        -----
        ret : dict
            api response json object
        """
        req_url = f"{self.url}/repos/{_group}/{_prj_name}"
        ret = requests.get(req_url, headers = self.req_header)
        return ret.json()


