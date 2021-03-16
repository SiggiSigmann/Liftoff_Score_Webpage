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
datadb = dbcon.DBconnector(socket.gethostbyname('db'),"networkdata", "test", "1234567")

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

### / ##########################################
@app.route("/", methods=["GET"])
def index_gett():
    return render_template('index.html')

#start server
if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=80)
