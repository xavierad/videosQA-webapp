'''
A video database application to serve proxy
confirm with professor: this flask will provide QA and user stats to proxy (however, proxy must know video_app urls)
'''

from flask import Flask, abort, request, redirect, url_for, session, jsonify, render_template
from time import sleep
from QandA_DB import *

app = Flask(__name__)


#                           Q&A DB ENDPOINTS
#-----------------------------------------------------------------------------
@app.route("/API/questions/<int:video_id>/", methods=['GET'])
def returnsQuestionsJSON(video_id):
    return {"questions": listQuestionsDICT(video_id)}

@app.route("/API/questions/<int:video_id>/", methods=['POST'])
def createNewQuestion(video_id):
    sleep(0.1)
    j = request.get_json()
    print (type(j))
    ret = False
    try:
        print(j["question"])
        ret = newQuestion(j["question"], j["user"], j["time"], j["video_id"])
    except:
        abort(400)
        #the arguments were incorrect
    if ret:
        return {"id": ret}
    else:
        abort(409)
    #if there is an erro return ERROR 409

@app.route("/API/questions/<int:video_id>/<int:question_id>/", methods=['GET'])
def returnsAnswersJSON(video_id, question_id):
    return {"answers": listAnswersDICT(question_id=question_id)}

@app.route("/API/questions/<int:video_id>/<int:question_id>/", methods=['POST'])
def createNewAnswer(video_id, question_id):
    sleep(0.1)
    j = request.get_json()
    print (type(j))
    ret = False
    try:
        print(j["answer"])
        ret = newAnswer(j["answer"], j["user_id"], j["user_name"], j["question_id"])
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
    # newAnswer('asd', '1')
    # print(listAnswersDICT(1))
    app.run(host='127.0.0.1', port=8002, debug=True)