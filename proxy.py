


# Alguns apontamentos
# REST API to manipulate resources: 
# videos, video list (endpoint or not?), creation of a video (through REST API form), list of questions and answers, user stats
# What are the endpoints to manipulate those resources (give a name), define what data is transferred between client/server
#
# all this in proxy: endpoints, resources and data


'''
Dúvidas:
( ) - 
( ) - 
( ) - 

A fazer:
( ) - 
( ) - 
( ) - 

'''

# -------------------------------------------------------------------------------------
#                   Architectures and Internet Systems Project 2020/2021
#
# Developed by Pedro Martin (87094) & Xavier Dias (87136)
# -------------------------------------------------------------------------------------

# - COMPONENTS OF PROXY:
# user web pages (admin and regular)
# authentication
# API
# Admin web pages

# -DEFINITIONS
# Resources: video, 
#            question,
#            answer,
#            user stats
# Operations that can be performed:
# (URI and Possible Methods, GET,POST,PATCH/PUT)

from flask import Flask, abort, request,  redirect, url_for
from Video_DB import *
from time import sleep

app = Flask(__name__)

# Proxy endpoints
#-----------------------------------------------------------------------------
# Related to videos

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
    # sleep(0.1)
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

# Related to videos
#-----------------------------------------------------------------------------
# Related to questions

# Related to questions
#-----------------------------------------------------------------------------
# Related to answers

# Related to answers
#-----------------------------------------------------------------------------
# Related to users

# Related to users
#-----------------------------------------------------------------------------

@app.route("/")
def index():
    return app.send_static_file('index.html')
    
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8000, debug=True)
