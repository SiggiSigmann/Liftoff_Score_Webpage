from flask import request, redirect
from flask import jsonify
from flask import Flask
from flask import render_template
from flask import Response
from flask import make_response
from flask import send_from_directory

import sys
import os
import socket
import io
import json
import datetime

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask_weasyprint import HTML, render_pdf

import dbconnector.dbconnector as dbcon

#init classes
#connect to db
db = dbcon.DBconnector(socket.gethostbyname('liftoff_db'),"LIFTOFF_DATA", "test", "1234567")

## Flask ##########################################################
#create flask server
app = Flask(__name__, template_folder=os.path.abspath('/html/'), static_folder=os.path.abspath('/static/'))

### robot.txt ####################
@app.route('/robots.txt')
def return_robots_txt():
    return app.send_static_file("robots.txt")

### humans.txt ####################
@app.route('/humans.txt')
def return_humans_txt():
    return app.send_static_file("humans.txt")

### manifest.webmanifest.txt ####################
#@app.route('/manifest.webmanifest')
#def return_manifest_txt():
#    return app.send_static_file("manifest.webmanifest")

### input #######################################
@app.route("/drone", methods=["GET"])
def get_drones():
    drones = db.getDrones()
    return render_template('drone.html', drones=drones)

@app.route("/drone", methods=["POST"])
def create_drone():
    response = request.form
    dronename = response["dronename"]
    #todo check username and collor using regex
    db.add_new_drone(dronename);    

    drones = db.getDrones()
    return render_template('drone.html', drones=drones)

@app.route("/result", methods=["GET"])
def get_result():
    results = db.getResult()
    return render_template('result.html', results=results)

@app.route("/result", methods=["POST"])
def create_result():
    response = request.form
    mapid = response["mapid"]
    trackid = response["trackid"]
    userid = response["userid"]
    droneid = response["droneid"]
    resulttimestamp = response["resulttimestamp"]
    print(resulttimestamp, file=sys.stderr)
    #todo check username and collor using regex
    db.add_new_result(mapid, trackid, userid, droneid, resulttimestamp);    
    
    results = db.getDrones()
    return render_template('result.html', results=results)

### user #######################################
@app.route("/users", methods=["GET"])
def user_get():
    users = db.getUsers()
    print(users, file=sys.stderr)

    return render_template('users.html', users=users)

@app.route("/users", methods=["POST"])
def create_user():
    response = request.form
    username = response["username"]
    usercolor = response["color"]
    #todo check username and collor using regex
    db.add_new_user(username, usercolor);    

    users = db.getUsers()
    return render_template('users.html', users=users)

### / ##########################################
@app.route("/", methods=["GET"])
def index_get():
    tracks = db.getTracks()
    print(tracks, file=sys.stderr)

    return render_template('index.html', tracks=tracks)

#start server
if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=80)
