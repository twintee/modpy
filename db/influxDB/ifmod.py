#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
from influxdb import InfluxDBClient

class influxClient:
    """influxDB Api handler class

    Attributes:
    ----------
        hndl : InfluxDBClient
            api handler
    """

    def __init__(self, _host, _user, _passwd, _db, _port=8086):
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
        self.hndl = InfluxDBClient(_host, _port, _user, _passwd, _db)

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

