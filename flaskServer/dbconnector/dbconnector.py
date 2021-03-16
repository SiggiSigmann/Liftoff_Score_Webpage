#!/usr/bin/python3

import pymysql
import socket
from datetime import datetime
import datetime
import threading
import sys
import json
import sys

# Database connector
class DBconnector:
    def __init__(self, address, database, user, pwd):
        self._address = address
        self._database = database
        self._user = user
        self._pwd = pwd
        self.db = None
        self.lock = threading.Lock()

        #check connection
        #will restart docker when fail
        self._connect()
        self._dissconect()

    #connect to db
    def _connect(self):
        if self.db is None:
            self.db = pymysql.connect(self._address, self._user, self._pwd, db=self._database)

    #dissconect db
    def _dissconect(self):
        if self.db is not None:
            self.db.close()
            self.db = None

    #get Track
    #read data out of DT
    def getTracks(self):
        self.lock.acquire()
        self._connect()
        
        with self.db.cursor() as cur:
            cur.execute('SELECT MAPS.mapname, TRACKS.trackname, TRACKS.hardness From TRACKS INNER JOIN MAPS ON TRACKS.mapid = MAPS.mapid;')
            tracks =  cur.fetchall()

        self._dissconect()
        self.lock.release()
        return tracks

    #get Track
    #read data out of DT
    def getUsers(self):
        self.lock.acquire()
        self._connect()
        
        with self.db.cursor() as cur:
            cur.execute('SELECT userid, username, usercolor From USERS;')
            users =  cur.fetchall()

        self._dissconect()
        self.lock.release()
        return users

    def add_new_user(self, username, color):
        self.lock.acquire()
        self._connect()
        
        with self.db.cursor() as cur:
            cur.execute('INSERT INTO USERS VALUES ( "'+username+'", "'+color+'");')
            users =  cur.fetchall()

        self._dissconect()
        self.lock.release()
        return users

