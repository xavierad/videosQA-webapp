# -------------------------------------------------------------------------------------
#                   Architectures and Internet Systems Project 2020/2021
#
# Developed by Pedro Martin (87094) & Xavier Dias (87136)
# -------------------------------------------------------------------------------------

import os 
from flask import Flask, abort, request, redirect, url_for, session, jsonify, render_template
from flask_dance.consumer import OAuth2ConsumerBlueprint
from time import sleep
import requests as rq
from datetime import datetime
from admin.admin import construct_admin_bp
from regular.regular import construct_regular_bp
import os.path

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.secret_key = "supersekrit"  # Replace this with your own secret!
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
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

# Registering blueprints: fenix, admin and regular
app.register_blueprint(fenix_blueprint)
app.register_blueprint(construct_admin_bp(fenix_blueprint), url_prefix="/admin")
app.register_blueprint(construct_regular_bp(fenix_blueprint), url_prefix="/regular")

# Target databases addresses
VIDEOS_URL = 'http://127.0.0.1:8000/API/'
USERS_URL = 'http://127.0.0.1:8001/API/'
QUESTIONS_URL = 'http://127.0.0.1:8002/API/'

# This functions allows to write log events on a file named log.txt
def write_to_log(f="log.txt", mode="w", endpoint="ENDPOINT", timestamp="TIMESTAMP", event="EVENT"):
    with open(f, mode) as log:    
        log.write('{: <20s} | {: <40s} | {:}\n\n'.format(timestamp, endpoint , event))

# Initializing log.txt
if not os.path.exists('log.txt'):
    write_to_log(mode="w")
    

#                           PROXY ENDPOINTS
#-----------------------------------------------------------------------------
# Related to login / logout

# To save id and name of the user logged in
class This_User:
    id = ''
    name = ''
this_user = This_User()


@app.route('/')
def home_page():
    # The access token is generated everytime the user authenticates into FENIX
    print(fenix_blueprint.session.authorized)
    # print("Access token: "+ str(fenix_blueprint.session.access_token))

    if fenix_blueprint.session.authorized == False:
        #if not logged in browser is redirected to login page (in this case FENIX handled the login)
        return render_template("appPage.html", loggedIn = fenix_blueprint.session.authorized, userID='', userName='')

    try:
        #if the user is authenticated then a request to FENIX is made
        resp = fenix_blueprint.session.get("/api/fenix/v1/person/")
        #res contains the responde made to /api/fenix/vi/person (information about current user)
        user = resp.json() 
        this_user.id = user['username']
        this_user.name = user['name']
        return render_template("appPage.html", loggedIn = fenix_blueprint.session.authorized, userID=user['username'], userName=user['name'])

    except:  
        #if not logged in browser is redirected to login page (in this case FENIX handled the login)
        return render_template("appPage.html", loggedIn = fenix_blueprint.session.authorized, userID='', userName='')


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

# Related to login / logout
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
        endpoint=url, event='List of video(s) dictionary returned ' + str(resp['videos'][:]))        

    return resp

# get a single video
@app.route("/API/videos/<int:id>/")
def returnSingleVideoJSON(id):
    url = VIDEOS_URL+'videos/'+str(id)
    resp = rq.get(url).json()

    # datetime object containing current date and time and converting it to a string
    now = datetime.now()    
    write_to_log(mode="a",timestamp=now.strftime("%d/%m/%Y %H:%M:%S"),
        endpoint=url, event='Single video dictionary returned ' + str(resp))  

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
            endpoint=url, event=f'User {this_user.id} registered a new video with id {ret}, dataype of dictionary, content {j}')  
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
        endpoint=url, event='List of question(s) dictionary returned ' + str(resp['questions'][:]))        

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
            endpoint=url, event=f'User {this_user.id} created a new question with id {ret}, Question datatype, content {j}')  
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
        endpoint=url, event='Answer(s) dictionary returned ' + str(resp['answers'][:]))        

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
            endpoint=url, event=f'User {this_user.id} created a new answer with id {ret}, Answer datatype, content {j} ')  
        print(ret)
        return {"id": ret}
    else:
        abort(409)
    #if there is an erro return ERROR 409

# Related to answers
#-----------------------------------------------------------------------------
# Related to users

# get a list of users registered
@app.route("/API/users/", methods=['GET'])
def returnsUsersJSON():
    url = USERS_URL + 'users/'
    resp = rq.get(url).json()
    
    # datetime object containing current date and time and converting it to a string
    now = datetime.now()    
    write_to_log(mode="a",timestamp=now.strftime("%d/%m/%Y %H:%M:%S"),
        endpoint=url, event='List of user(s) dictionary returned ' + str(resp['users'][:]))        

    return resp

# get a single user
@app.route("/API/users/<string:id>/")
def returnSingleUserJSON(id):
    url = USERS_URL+'users/'+(id)+'/'
    resp = rq.get(url).json()

    # datetime object containing current date and time and converting it to a string
    now = datetime.now()    
    write_to_log(mode="a",timestamp=now.strftime("%d/%m/%Y %H:%M:%S"),
        endpoint=url, event='Single user dictionary returned ' + str(resp))  

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
        abort(400)
        #the arguments were incorrect

    if ret != {}:
        now = datetime.now()    
        write_to_log(mode="a",timestamp=now.strftime("%d/%m/%Y %H:%M:%S"),
            endpoint=url, event=f'Created new user {ret}, User datatype , content {j}')  
        print(ret)
        return {"id": ret}
    elif ret == {}:
        print('User already exists...')
        return {}
    else:
        abort(409)
    #if there is an erro return ERROR 409

# increment the number of registered videos of an user
@app.route("/API/users/<string:user_id>/videosRegistred/", methods=['PUT', 'PATCH'])
def newVideoRegistration(user_id):
    url = USERS_URL+'users/'+user_id+'/videosRegistred/'
    ret = rq.put(url, user_id).json()

    # datetime object containing current date and time and converting it to a string
    now = datetime.now()    
    write_to_log(mode="a",timestamp=now.strftime("%d/%m/%Y %H:%M:%S"),
        endpoint=url, event='Number of video registrations by user '+ user_id +' uptated to '+ str(ret))  

    return ret

# increment the number of videos visualized by an user
@app.route("/API/users/<string:user_id>/videoViews/", methods=['PUT', 'PATCH'])
def incrementUserViews(user_id):
    url = USERS_URL+'users/'+user_id+'/videoViews/'
    ret = rq.put(url, user_id).json()

    # datetime object containing current date and time and converting it to a string
    now = datetime.now()    
    write_to_log(mode="a",timestamp=now.strftime("%d/%m/%Y %H:%M:%S"),
        endpoint=url, event='Number of views of user ' + user_id +' updated to ' + str(ret))  

    return ret

# increment the number of questions made by an user
@app.route("/API/users/<string:user_id>/nquestions/", methods=['PUT', 'PATCH'])
def incrementUserQuestions(user_id):
    url = USERS_URL+'users/'+user_id+'/nquestions/'
    ret = rq.put(url, user_id).json()
    
    # datetime object containing current date and time and converting it to a string
    now = datetime.now()    
    write_to_log(mode="a",timestamp=now.strftime("%d/%m/%Y %H:%M:%S"),
        endpoint=url, event='Number of questions made by ' + user_id + ' updated to ' + str(ret))  

    return ret

# increment the number of answers made by an user
@app.route("/API/users/<string:user_id>/nanswers/", methods=['PUT', 'PATCH'])
def incrementUserAnswers(user_id):
    url = USERS_URL+'users/'+user_id+'/nanswers/'
    ret = rq.put(url, user_id).json()
        
    # datetime object containing current date and time and converting it to a string
    now = datetime.now()    
    write_to_log(mode="a",timestamp=now.strftime("%d/%m/%Y %H:%M:%S"),
        endpoint=url, event='Number of answers made by ' + user_id + ' updated to ' + str(ret))  

    return ret

# Related to users
#-----------------------------------------------------------------------------

if __name__ == "__main__":
   app.run(debug=True) # by default it will run in 127.0.0.1:5000
