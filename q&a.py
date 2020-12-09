'''
A video database application to serve proxy
confirm with professor: this flask will provide QA and user stats to proxy (however, proxy must know video_app urls)
'''

from flask import Flask, abort, request, redirect, url_for, session, jsonify, render_template
from time import sleep
from Q&A_DB import *

app = Flask(__name__)


#                           Q&A DB ENDPOINTS
#-----------------------------------------------------------------------------
# get a list of questions
@app.route("/API/questions/", methods=['GET'])
def returnsQuestionJSON():
    return {"questions": listQuestionDICT()}

# get a single question
@app.route("/API/questions/<int:id>/")
def returnSingleQuestionJSON(id):
    try:
        v = getQuestionDICT(id)
        return v
    except:
        abort(404)

# create a new question
@app.route("/API/questions/", methods=['POST'])
def createNewQuestion():
    sleep(0.1)
    j = request.get_json()
    print(j)
    print (type(j))
    ret = False
    try:
        print(j["url"])
        # ret = newVideo(j["description"], j['url'])
    except:
        abort(400)
        #the arguments were incorrect
    if ret:
        return {"id": ret}
    else:
        abort(409)
    #if there is an erro return ERROR 409

    
@app.route("/")
def index():
    pass
    # return app.send_static_file('index.html')
    
if __name__ == "__main__":
   app.run(host='127.0.0.1', port=8002, debug=True)