from flask import request, redirect
from flask import jsonify
from flask import Flask
from flask import render_template
from flask import Response
from flask import make_response
from flask import send_from_directory
from flask import url_for

import sys
import os
import socket
import io
import json
import datetime
import re
from werkzeug.utils import secure_filename

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask_weasyprint import HTML, render_pdf

from excleLoader import ExcelLoader

import dbconnector.dbconnector as dbcon

#init classes
#connect to db
db = dbcon.DBconnector(socket.gethostbyname('liftoff_db'),"LIFTOFF_DATA", "test", "1234567")

loader = ExcelLoader(db)

## Flask ##########################################################
#create flask server
app = Flask(__name__, template_folder=os.path.abspath('/html/'), static_folder=os.path.abspath('/static/'))
UPLOAD_FOLDER = './temp'
ALLOWED_EXTENSIONS = {'xlsx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    drones = db.get_drones()
    return render_template('drone.html', active="drones", drones=drones, success = 2)

@app.route("/drone", methods=["POST"])
def create_drone():
    response = request.form
    dronename = response["dronename"]
    
    success = 0
    if len(dronename) < 26:
        success = 1
        try:
            db.add_new_drone(dronename)
        except:
            #print("drone error while insertion", file=sys.stderr)
            success = 0

    drones = db.get_drones()
    return render_template('drone.html', active="drones", drones=drones, success=success)

@app.route("/result", methods=["GET"])
def get_result():
    results = db.get_results()
    users = db.get_users()
    drones = db.get_drones()
    maps = db.get_maps()
    tracks = db.get_tracks()
    return render_template('result.html', active="results", results=results, users=users, drones=drones, maps=maps, tracks=tracks, success = 2)

@app.route("/result", methods=["POST"])
def create_result():
    response = request.form
    mapid = int(response["mapid"])
    trackid = int(response["trackid"])
    userid = int(response["userid"])
    droneid = int(response["droneid"])
    resulttimestamp = response["resulttimestamp"]

    success = 1
    maps = db.get_maps()
    if not (len(maps) >= mapid and 0 < mapid):
        success = 0

    tracks = db.get_tracks()
    if not (len(tracks["maps"][mapid-1]["tracks"]) >= trackid and 0 < trackid):
        success = 0

    users = db.get_users()
    if not (len(users) >= int(userid) and 0 < userid):
        success = 0
    
    drones = db.get_drones()
    if not (len(drones) >= droneid and 0 < droneid):
        success = 0


    matched = re.match("[0-9]{2}:[0-9]{2}:[0-9]{3}", resulttimestamp)
    if not bool(matched):
        success = 0
    
    #==>
    #print("insert", file=sys.stderr)
    if success == 1:
        try:
            db.add_new_result(mapid, trackid, userid, droneid, resulttimestamp)
        except:
           # print("result error whil insertion", file=sys.stderr)
            success = 0

    results = db.get_results()
    return render_template('result.html', active="results", results=results, users=users, drones=drones, maps=maps, tracks=tracks, success=success)

#todo:
#get only most reson results
#display themn in combination wit the index page
### user #######################################
@app.route("/users", methods=["GET"])
def user_get():
    users = db.get_users()

    return render_template('users.html',active="users", users=users, success = 2)

@app.route("/users", methods=["POST"])
def create_user():
    response = request.form
    username = response["username"]
    usercolor = response["color"]
    success = 0
    if len(username) <=25 and len(username) > 0:
        success = 1

        try:
            db.add_new_user(username, usercolor)
        except:
           # print("user error while insertion", file=sys.stderr)
            success = 0

    users = db.get_users()
    return render_template('users.html', active="users", users=users, success = success)

### imex ########################################
@app.route("/imex", methods=["GET"])
def imex_get():
    return render_template('imex.html', active="imex")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/imex', methods=['POST'])
def upload_file():
    #print("upload", file=sys.stderr)
    # check if the post request has the file part
    if 'file' not in request.files:
        return render_template('imex.html', active="imex", error=-1)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return render_template('imex.html', active="imex", error=-2)
    if file and allowed_file(file.filename):
        #file was uploaded
        filename = secure_filename(file.filename)
        #print(filename, file=sys.stderr)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        success = loader.loadFile(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))

       
        return render_template('imex.html', active="imex", error=success)

    return render_template('imex.html', active="imex", error=105)

@app.route("/random", methods=["GET"])
def random_get():
    tracks = db.get_tracks()
    users = db.get_users()
    best_results = db.get_best_reslt_per_user()
    drone_list = db.get_drones()
    return render_template('random.html', active="random", tracks=tracks, users=users, best_results=best_results, drone_list=drone_list)

@app.route("/random", methods=["POST"])
def random_add():
    
    mapid = request.form["mapid"]
    trackid = request.form["trackid"]
    droneid = request.form["droneid"]

    success = 1
    users = db.get_users()
    for user in users:
        userid = user[0]
    
        resulttimestamp = request.form[str(userid)]

        if resulttimestamp != None and resulttimestamp != '':

            matched = re.match("[0-9]{2}:[0-9]{2}:[0-9]{3}", resulttimestamp)
            if not bool(matched):
                success = 0

            if success == 1:
                db.add_new_result(mapid, trackid, userid, droneid, resulttimestamp)


    tracks = db.get_tracks()

    best_results = db.get_best_reslt_per_user()
    return render_template('random.html', active="random", tracks=tracks, users=users, best_results=best_results, success=success)

@app.route("/breakingpilot", methods=["GET"])
def breakingpilot_get():
    breaking = db.get_breaking()
    users = db.get_users()
    return render_template('breakingpilot.html', active="breakingpilot", breaking=breaking, users=users, success=-1)

@app.route("/breakingpilot", methods=["POST"])
def breakingpilot_post():
    userid = request.form["userid"]
    mode = request.form["mode"]

    db.add_breaking(userid, mode)

    breaking = db.get_breaking()
    users = db.get_users()
    return render_template('breakingpilot.html', active="breakingpilot", breaking=breaking, users=users, success=1)


### / ##########################################
@app.route("/", methods=["GET"])
def index_get():
    tracks = db.get_tracks()
    best_results = db.get_best_reslt_per_user()
    users = db.get_users()
    drone_list = db.get_drones()

    return render_template('index.html', active="overview",tracks=tracks, users=users, best_results=best_results, drone_list= drone_list)

#start server
if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=80)
