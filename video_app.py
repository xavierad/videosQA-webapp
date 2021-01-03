'''
A video database application to serve proxy
'''

from flask import Flask, abort, request, redirect, url_for, session, jsonify, render_template
from time import sleep
from Video_DB import *

app = Flask(__name__)

#                           VIDEO DB ENDPOINTS
#-----------------------------------------------------------------------------
# get a list of videos
@app.route("/API/videos/", methods=['GET'])
def returnsVideosJSON():
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
    print(j)
    print (type(j))
    ret = False
    try:
        print(j["url"])
        ret = newVideo(j["description"], j['url'])
    except:
        abort(400)
        #the arguments were incorrect
    if ret:
        return {"id": ret}
    else:
        abort(409)
    #if there is an erro return ERROR 409

# to increment the number of views
@app.route("/API/videos/<int:id>/views", methods=['PUT', 'PATCH'])
def newView(id):
    try:
        return {"id":id, "views": newVideoView(id)}
    except:
        abort(404)

    
if __name__ == "__main__":
   app.run(host='127.0.0.1', port=8000, debug=True)