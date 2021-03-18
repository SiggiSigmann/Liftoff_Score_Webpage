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

    def add_new_user(self, username, usercolor):
        self.lock.acquire()
        self._connect()
        
        with self.db.cursor() as cur:
            cur.execute('INSERT INTO USERS (username ,usercolor) VALUES ( "'+username+'", "'+usercolor+'");')

        self.db.commit()
        self._dissconect()
        self.lock.release()

    def getDrones(self):
        self.lock.acquire()
        self._connect()
        
        with self.db.cursor() as cur:
            cur.execute('SELECT droneid, dronename From DRONES;')
            users =  cur.fetchall()

        self._dissconect()
        self.lock.release()
        return users

    def add_new_drone(self, dronename):
        self.lock.acquire()
        self._connect()
        
        with self.db.cursor() as cur:
            cur.execute('INSERT INTO DRONES (dronename) VALUES ( "'+dronename+'");')

        self.db.commit()
        self._dissconect()
        self.lock.release()

    def getResult(self):
        self.lock.acquire()
        self._connect()
        
        with self.db.cursor() as cur:
            cur.execute('SELECT mapid, trackid, userid, droneid, resulttimestamp From RESULTS;')
            users =  cur.fetchall()

        self._dissconect()
        self.lock.release()
        return users

    def add_new_result(self, mapid, trackid, userid, droneid, resulttimestamp):
        self.lock.acquire()
        self._connect()
        
        with self.db.cursor() as cur:
            cur.execute('INSERT INTO RESULTS (mapid, trackid, userid, droneid, resulttimestamp) '+\
                        'VALUES ( "'+mapid+'", "'+trackid+'", "'+userid+'", "'+droneid+'", "'+resulttimestamp+'");')

        self.db.commit()
        self._dissconect()
        self.lock.release()

