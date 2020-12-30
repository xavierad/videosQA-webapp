'''
A user manager database application to serve proxy
'''

from flask import Flask, abort, request, redirect, url_for, session, jsonify, render_template, Response
from time import sleep
from User_DB import *

app = Flask(__name__)


#                           USER DB ENDPOINTS
#-----------------------------------------------------------------------------
# get a list of users
@app.route("/API/users/", methods=['GET'])
def returnsUsersJSON():
    return {"users": listUsersDICT()}

# get a single user
@app.route("/API/users/<int:id>/")
def returnSingleUserJSON(id):
    try:
        usr = getUserDICT(id)
        return usr
    except:
        abort(404)

@app.route("/API/users/<string:user_id>/videosRegistred/", methods=['PUT', 'PATCH'])
def newVideoRegistration(user_id):
    try:
        return {"user_id":user_id, "videoRegistrations": newVideoRegist(user_id)}
    except Exception as e:
        print(e)
        abort(404)

# create a new user
@app.route("/API/users/", methods=['POST'])
def createNewUser():
    sleep(0.1)
    j = request.get_json()
    print(j)
    print (type(j))
    ret = False
    try:
        print(j["id"])
        ret = newUser(j['id'], j['name'])
    except:
        abort(400)
        #the arguments were incorrect
    if ret != {}:
        return {"id": ret}
    else:        
        return {}
    # if there is an erro return ERROR 409


    
@app.route("/")
def index():
    pass
    # return app.send_static_file('index.html')
    
if __name__ == "__main__":
   app.run(host='127.0.0.1', port=8001, debug=True)