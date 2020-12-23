





'''
Dúvidas:
( ) - 308 response?
( ) - can log be only global variable present in proxy? 
(X) - confirm extensibility logic of video_app
( ) - index.html porquÊ no static e não no template?
( ) - login: token and takes too much time
( ) - when an user wants to add new question he must click on New Question and video should be paused. Can we make it otherwise (pause to be able que add new question)?
( ) - 


A fazer:
(X) - videos request endpoints
(X) - videos list page
(X) - video page (watch and count view (not for a user particulary))
(X) - proxy endpoints related to user manager
( ) - TO FIX: when entered on admin page, token is taken again (but it's not necessary)
( ) - 
( ) - 
( ) - 

Notas: 
- VideoDb cannot be simply imported to proxy and its methods to be called. It would be like we were implementing all in proxy and this does not satisfy extensibility
Probably we must tranfor videoDb into a flask app in order to interact with proxy through REST.
- REST API to manipulate resources: 
videos, video list (endpoint or not?), creation of a video (through REST API form), list of questions and answers, user stats
What are the endpoints to manipulate those resources (give a name to each resource), define what data is transferred between client/server
all this in proxy: endpoints, resources and data
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
#
# - DEFINITIONS
# Resources: 
# 1) video, 
# 2) question,
# 3) answer,
# 4) user manager,
# 5) logs (is it?)
#
# Operations that can be performed: 
# 1) new video (POST), get a video (POST), get the list of videos (GET),
# 2) new question (POST), view a question (all info regarding it) (GET), list of questions (GET),
# 3) new answer (POST), view a answer (is necessary?) (GET), list of answers (GET),
# 4) 
#            
# (URI and Possible Methods, GET,POST,PATCH/PUT)
#ist14021 - João Silva

import os 
from flask import Flask, abort, request, redirect, url_for, session, jsonify, render_template
from flask_dance.consumer import OAuth2ConsumerBlueprint
from time import sleep
import requests as rq
from datetime import datetime
from admin.admin import construct_admin_bp
from regular.regular import construct_regular_bp

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.secret_key = "supersekrit"  # Replace this with your own secret!
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False

# apagar no final do projeto os ifs
import sys
fenix_id = ''
if len(sys.argv) > 1 :
    fenix_id = sys.argv[1]
if fenix_id == '' or fenix_id == 'pedro':
    # Pedro
    print(fenix_id)
    fenix_blueprint = OAuth2ConsumerBlueprint(
        "fenix-example", __name__,
        # this value should be retrived from the FENIX OAuth page
        client_id="1695915081466076",
        # this value should be retrived from the FENIX OAuth page
        client_secret="TOxHh4DiSz/Z6hT+kRKASmJ5cmDD3dSPm79J+ikRtG991k09qypy29v7EZQsP82kV3tM2MPxfKXbm7mJop7KMg==",
        # do not change next lines
        base_url="https://fenix.tecnico.ulisboa.pt/",
        token_url="https://fenix.tecnico.ulisboa.pt/oauth/access_token",
        authorization_url="https://fenix.tecnico.ulisboa.pt/oauth/userdialog",
    )
elif fenix_id=='xavier':
    print(fenix_id)
    fenix_blueprint = OAuth2ConsumerBlueprint(
        "fenix-example", __name__,
        # this value should be retrived from the FENIX OAuth page
        client_id="1132965128044779",
        # this value should be retrived from the FENIX OAuth page
        client_secret="HOmZwGuoFApLQEdqum3DTdSMk6XpLux6qJoqhZZVrKRQ+0cqo/rBnAupdik01GLsqunxF2EIR2jYef8skOS3Jg==",
        # do not change next lines
        base_url="https://fenix.tecnico.ulisboa.pt/",
        token_url="https://fenix.tecnico.ulisboa.pt/oauth/access_token",
        authorization_url="https://fenix.tecnico.ulisboa.pt/oauth/userdialog",
    )
else:
    sys.exit()

user = {}
app.register_blueprint(fenix_blueprint)
app.register_blueprint(construct_admin_bp(fenix_blueprint), url_prefix="/admin")
app.register_blueprint(construct_regular_bp(fenix_blueprint), url_prefix="/regular")


# Target databases addresses
VIDEOS_URL = 'http://127.0.0.1:8000/API/'
USERS_URL = 'http://127.0.0.1:8001/API/'
QUESTIONS_URL = 'http://127.0.0.1:8002/API/'


# A log file that will store all events ocurred in the system
def write_to_log(f="log.txt", mode="w", timestamp="TIMESTAMP", event="EVENT"):
    with open(f, mode) as log:    
        log.write('{: <20s} : {:}\n\n'.format(timestamp, event))

# Initialize log.txt
write_to_log(mode="w")
    

#                           PROXY ENDPOINTS
#-----------------------------------------------------------------------------
# Related to login

@app.route('/')
def home_page():
    # The access token is generated everytime the user authenticates into FENIX
    print(fenix_blueprint.session.authorized)
    print("Access token: "+ str(fenix_blueprint.session.access_token))

    if fenix_blueprint.session.authorized == False:
        #if not logged in browser is redirected to login page (in this case FENIX handled the login)
        return render_template("appPage.html", loggedIn = fenix_blueprint.session.authorized)

    #if the user is authenticated then a request to FENIX is made
    resp = fenix_blueprint.session.get("/api/fenix/v1/person/")
    #res contains the responde made to /api/fenix/vi/person (information about current user)
    user = resp.json() 
    print(resp.json())
           
    return render_template("appPage.html", loggedIn = fenix_blueprint.session.authorized, userID=user['username'], userName=user['name'])

@app.route('/logout')
def logout():
    # this clears all server information about the access token of this connection
    res = str(session.items())
    print(res)
    session.clear()
    res = str(session.items())
    print(res)
    # when the browser is redirected to home page it is not logged in anymore
    return redirect(url_for("home_page"))    

# Related to login
#-----------------------------------------------------------------------------
# Related to videos

# get a list of videos
@app.route("/API/videos/", methods=['GET'])
def returnsVideosJSON():
    url = VIDEOS_URL + 'videos'
    resp = rq.get(url).json()
    
    # datetime object containing current date and time and converting it to a string
    now = datetime.now()    
    write_to_log(mode="a",timestamp=now.strftime("%d/%m/%Y %H:%M:%S"),
        event='Videos dictionary returned ' + str(resp['videos'][:]))        

    return resp

# get a single video
@app.route("/API/videos/<int:id>/")
def returnSingleVideoJSON(id):
    url = VIDEOS_URL+'videos/'+str(id)
    resp = rq.get(url).json()

    # datetime object containing current date and time and converting it to a string
    now = datetime.now()    
    write_to_log(mode="a",timestamp=now.strftime("%d/%m/%Y %H:%M:%S"),
        event='Single video dictionary returned ' + str(resp))  

    return resp

# create a new video
@app.route("/API/videos/", methods=['POST'])
def createNewVideo():
    url = VIDEOS_URL+'videos/'
    j = request.get_json()
    print(j)
    try:
        print(j["description"])
        ret = rq.post(url, json=j).json()
    except:
        abort(400)
        #the arguments were incorrect
    if ret:
        now = datetime.now()    
        write_to_log(mode="a",timestamp=now.strftime("%d/%m/%Y %H:%M:%S"),
            event='Created new video with id ' + str(ret))  
        print(ret)
        return {"id": ret}
    else:
        abort(409)
    #if there is an erro return ERROR 409

@app.route("/API/videos/<int:id>/views", methods=['PUT', 'PATCH'])
def newView(id):
    ret = rq.put(VIDEOS_URL+'videos/'+str(id)+'/views', str(id)).json()
    return ret

# Related to videos
#-----------------------------------------------------------------------------
# Related to questions

# get a list of questions
@app.route("/API/questions/<int:video_id>/", methods=['GET'])
def returnsQuestionsJSON(video_id):
    url = QUESTIONS_URL + 'questions/'+str(video_id)+'/'
    resp = rq.get(url).json()
    
    # datetime object containing current date and time and converting it to a string
    now = datetime.now()    
    write_to_log(mode="a",timestamp=now.strftime("%d/%m/%Y %H:%M:%S"),
        event='Questions dictionary returned ' + str(resp['questions'][:]))        

    return resp

# create a new question
@app.route("/API/questions/<int:video_id>/", methods=['POST'])
def createNewQuestion(video_id):
    url = QUESTIONS_URL+'questions/'+str(video_id)+'/'
    j = request.get_json()
    print(j)
    try:
        print(j["question"])
        ret = rq.post(url, json=j).json()
    except:
        abort(400)
        #the arguments were incorrect
    if ret:
        now = datetime.now()    
        write_to_log(mode="a",timestamp=now.strftime("%d/%m/%Y %H:%M:%S"),
            event='Created new question with id ' + str(ret))  
        print(ret)
        return {"id": ret}
    else:
        abort(409)
    #if there is an erro return ERROR 409

# Related to questions
#-----------------------------------------------------------------------------
# Related to answers

# get a list of answers regarding a question
@app.route("/API/questions/<int:video_id>/<int:question_id>/", methods=['GET'])
def returnsAnswersJSON(video_id, question_id):
    url = QUESTIONS_URL + 'questions/'+str(video_id)+'/'+str(question_id)+'/'
    resp = rq.get(url).json()
    
    # datetime object containing current date and time and converting it to a string
    now = datetime.now()    
    write_to_log(mode="a",timestamp=now.strftime("%d/%m/%Y %H:%M:%S"),
        event='Answer(s) dictionary returned ' + str(resp['answers'][:]))        

    return resp

# create a new answer
@app.route("/API/questions/<int:video_id>/<int:question_id>/", methods=['POST'])
def createNewAnswer(video_id, question_id):
    url = QUESTIONS_URL+'questions/'+str(video_id)+'/'+str(question_id)+'/'
    j = request.get_json()
    print(j)
    try:
        print(j["answer"])
        ret = rq.post(url, json=j).json()
    except:
        abort(400)
        #the arguments were incorrect
    if ret:
        now = datetime.now()    
        write_to_log(mode="a",timestamp=now.strftime("%d/%m/%Y %H:%M:%S"),
            event='Created new answer with id ' + str(ret))  
        print(ret)
        return {"id": ret}
    else:
        abort(409)
    #if there is an erro return ERROR 409

# Related to answers
#-----------------------------------------------------------------------------
# Related to users

# get a list of users registered
@app.route("/API/users", methods=['GET'])
def returnsUsersJSON():
    url = USERS_URL + 'users'
    resp = rq.get(url).json()
    
    # datetime object containing current date and time and converting it to a string
    now = datetime.now()    
    write_to_log(mode="a",timestamp=now.strftime("%d/%m/%Y %H:%M:%S"),
        event='Users dictionary returned ' + str(resp['users'][:]))        

    return resp

# get a single user
@app.route("/API/users/<int:id>/")
def returnSingleUserJSON(id):
    url = USERS_URL+'users/'+str(id)
    resp = rq.get(url).json()

    # datetime object containing current date and time and converting it to a string
    now = datetime.now()    
    write_to_log(mode="a",timestamp=now.strftime("%d/%m/%Y %H:%M:%S"),
        event='Single user dictionary returned ' + str(resp))  

    return resp

# create a new user
@app.route("/API/users/", methods=['POST'])
def createNewUser():
    url = USERS_URL+'users/'
    j = request.get_json()
    print(j)
    try:
        print(j["id"])
        ret = rq.post(url, json=j).json()
    except Exception as e:
        print(e)
        abort(400)
        #the arguments were incorrect

    if ret != {}:
        now = datetime.now()    
        write_to_log(mode="a",timestamp=now.strftime("%d/%m/%Y %H:%M:%S"),
            event='Created new user ' + str(ret))  
        print(ret)
        return {"id": ret}
    elif ret == {}:
        print('User already exists...')
        return {}
    else:
        abort(409)
    #if there is an erro return ERROR 409

# Related to users
#-----------------------------------------------------------------------------




if __name__ == "__main__":
   app.run(debug=True) # by default it will run in 127.0.0.1:5000
