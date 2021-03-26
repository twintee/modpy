#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
from os.path import isfile, isdir, join, dirname, abspath, splitext
import sys
from influxdb import InfluxDBClient

sys.path.append(abspath(join(dirname(__file__), '..', '..')))
from loader.env_loader import EnvLoader

class InfluxDbHandler:
    """influxDB Api handler class

    Attributes:
    ----------
        hndl : InfluxDBClient
            api handler
    """

    def __init__(self,
            _host:str=None,
            _user:str=None,
            _passwd:str=None,
            _db:str=None,
            _port=8086,
            _envfile:str=".env"):
        """
        constructor

        Parameters
        -----
        _url : str
            host name
        _user : str
            username
        _passwd : str
            username
        _db : str
            reference database name
        _port : int
            port number
        """
        self.ifinfo = {
            'port': _port,
        }

        dir_script = abspath(dirname(__file__))
        path_env = join(dir_script, _envfile)

        # envがあれば初期値読み込み
        self.env = EnvLoader(path_env)
        if isfile(path_env):
            print(f"[info] get ifinfo from: {path_env}")
            self.ifinfo["host"] = self.env.get("host")
            self.ifinfo["port"] = self.env.get("port")
            self.ifinfo["user"] = self.env.get("user")
            self.ifinfo["password"] = self.env.get("password")
            self.ifinfo["db"] = self.env.get("db")

        # 引数上書き
        if not _host is None:
            self.ifinfo["url"] = _host
        if not _port is None:
            self.ifinfo["port"] = _port
        if not _user is None:
            self.ifinfo["user"] = _user
        if not _passwd is None:
            self.ifinfo["password"] = _passwd
        if not _db is None:
            self.ifinfo['db'] = _db

        self.hndl = InfluxDBClient(self.ifinfo['host'],
                self.ifinfo['port'],
                self.ifinfo['user'],
                self.ifinfo['password'],
                self.ifinfo['db'])
        self.env.save(_params=self.ifinfo)

        self.create_db(_db)

    def create_db(self, _db):
        """
        create database

        Parameters
        -----
        _db : str
            reference database name
        """

        # databaseの存在を判定し、作成前であれば新規作成
        dbs = self.hndl.get_list_database()
        ref_db = {'name' : _db}
        if ref_db not in dbs:
            self.hndl.create_database(_db)

    def write_points(self, _measurement, _fields, _tags):

        """
        insert records

        Parameters
        -----
        _fields : object
            insert fields as key and value sets
        _tags : object
            record tags as key and value sets
        _measurement : str
            insert fields as key and value sets
        """

        # インポートするjsonデータを作成
        import_data = [
            {
            "fields" : _fields,
            "tags" : _tags,
            "measurement" : _measurement,
            }
        ]
        # データ投入
        self.hndl.write_points(import_data)

    def get_points(self, _query):
        """
        get points

        Returns
        -----
        ret : dict
            api response json object
        """
        ret = self.hndl.query(_query)

        return ret

