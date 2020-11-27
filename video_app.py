'''
A video database application to serve proxy
confirm with professor: this flask will provide QA and user stats to proxy (however, proxy must know video_app urls)
'''

from flask import Flask, abort, request, redirect, url_for, session, jsonify, render_template
import requests as rq
from time import sleep
from Video_DB import *

app = Flask(__name__)


#                           VIDEO DB ENDPOINTS
#-----------------------------------------------------------------------------
# get a list of videos
@app.route("/API/videos/", methods=['GET'])
def returnsVideosJSON():
    with open(log.txt, "a") as log:
        # datetime object containing current date and time and converting it to a string
        now = datetime.now()       
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print("date and time = ", dt_string)	
        log.write(dt_string + ' | ' + 'Videos dictionary returned' + str(listVideosDICT()) + '\n')

    return {"videos": listVideosDICT()}

# get a single video
@app.route("/API/videos/<int:id>/")
def returnSingleVideoJSON(id):
    try:
        v = getVideoDICT(id)
        return v
    except:
        abort(404)

# create a new video
@app.route("/API/videos/", methods=['POST'])
def createNewVideo():
    sleep(0.1)
    j = request.get_json()
    print (type(j))
    ret = False
    try:
        print(j["description"])
        ret = newVideo(j["description"], j['url'])
    except:
        abort(400)
        #the arguments were incorrect
    if ret:
        return {"id": ret}
    else:
        abort(409)
    #if there is an erro return ERROR 409

@app.route("/API/videos/<int:id>/views", methods=['PUT', 'PATCH'])
def newView(id):
    try:
        return {"id":id, "views": newVideoView(id)}
    except:
        abort(404)
    
@app.route("/")
def index():
    return app.send_static_file('index.html')
    
if __name__ == "__main__":
   app.run(host='127.0.0.1', port=8000, debug=True)