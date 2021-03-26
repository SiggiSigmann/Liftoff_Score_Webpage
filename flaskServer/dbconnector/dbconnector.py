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
    transaction = 0

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
    #read data out of DB
    def get_tracks(self):
        self.lock.acquire()
        self._connect()
        
        track_json = '{"maps":['
        

        with self.db.cursor() as cur:
            cur.execute('SELECT MAPS.mapid, MAPS.mapname, TRACKS.trackid, TRACKS.trackname, TRACKS.hardness From TRACKS INNER JOIN MAPS ON TRACKS.mapid = MAPS.mapid;')
            tracks =  cur.fetchall()
            sorted_tracks = {}

            for track in tracks:
                if (track[0],track[1]) not in sorted_tracks.keys():
                    sorted_tracks[(track[0],track[1])] = []
  
                sorted_tracks[(track[0],track[1])].append(track[2:])


            
        for maps in sorted_tracks.keys():
            track_json += '{"mapid":'+str(maps[0])+', "mapname":"'+maps[1] +'", "tracks":['

            for track in sorted_tracks[maps]:
                track_json += '{"trackid":'+str(track[0])+',"trackname":"'+str(track[1])+'","hardness":'+str(track[2])+"},"

            track_json = track_json[:-1]
            track_json += "]},"
        track_json = track_json[:-1]

        track_json += ']}'

        self._dissconect()
        self.lock.release()
        return json.loads(track_json)

    #get Track
    #read data out of DT
    def get_users(self):
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
            cur.execute('INSERT INTO USERS (username ,usercolor) VALUES ( "'+str(username)+'", "'+str(usercolor)+'");')

        self.db.commit()
        self._dissconect()
        self.lock.release()

    def get_drones(self):
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
            cur.execute('INSERT INTO DRONES (dronename) VALUES ( "'+str(dronename)+'");')

        self.db.commit()
        self._dissconect()
        self.lock.release()

    def get_results(self):
        self.lock.acquire()
        self._connect()
        
        with self.db.cursor() as cur:
            cur.execute('SELECT mapid, trackid, userid, droneid, resulttimestamp From RESULTS;')
            users =  cur.fetchall()

        self._dissconect()
        self.lock.release()
        return users

    def get_best_reslt_per_user(self):
        self.lock.acquire()
        self._connect()

        json_container = {}
        
        with self.db.cursor() as cur:
            cur.execute('select droneid, mapid, trackid, userid,  min(resulttimestamp) from RESULTS group by mapid, trackid, userid, droneid;')
            best_results =  cur.fetchall()

            for result in best_results:
                #for maps
                if not result[0] in json_container.keys():
                    json_container[result[0]] = {}

                if not result[1] in json_container[result[0]].keys():
                    json_container[result[0]][result[1]] = {}

                if not result[2] in json_container[result[0]][result[1]].keys():
                    json_container[result[0]][result[1]][result[2]] = {}

                json_container[result[0]][result[1]][result[2]][result[3]] = result[4]

        print(json_container, file=sys.stderr)

                

        self._dissconect()
        self.lock.release()
        return json_container

    def add_new_result(self, mapid, trackid, userid, droneid, resulttimestamp):
        self.lock.acquire()
        self._connect()
        
        #get Date and time  (2020-11-04 10:40:00)
        now = datetime.datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

        with self.db.cursor() as cur:
            cur.execute('INSERT INTO RESULTS (mapid, trackid, userid, droneid, resulttimestamp, resultfrom) '+\
                        'VALUES ( '+str(mapid)+', '+str(trackid)+', '+str(userid)+', '+str(droneid)+', "'+str(resulttimestamp)+'", "'+dt_string+'");')

        self.db.commit()
        self._dissconect()
        self.lock.release()

    def get_maps(self):
        self.lock.acquire()
        self._connect()
        
        with self.db.cursor() as cur:
            cur.execute('SELECT mapid, mapname From MAPS;')
            users =  cur.fetchall()

        self._dissconect()
        self.lock.release()
        return users

    def get_map_track_id(self, mapname, trackname):
        self.lock.acquire()
        self._connect()
        
        with self.db.cursor() as cur:
            cur.execute('SELECT MAPS.mapid, TRACKS.trackid From TRACKS INNER JOIN MAPS ON TRACKS.mapid = MAPS.mapid '+\
                        'where MAPS.mapname = "'+mapname+'" and TRACKS.trackname ="'+trackname+'";')
            tracks =  cur.fetchall()
            if len(tracks) == 0:
                print(mapname+' and TRACKS.trackname ="'+trackname , file=sys.stderr)
                tracks = [[]]
        

        self._dissconect()
        self.lock.release()
        return tracks[0]
