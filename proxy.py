


# Alguns apontamentos
# REST API to manipulate resources: 
# videos, video list (endpoint or not?), creation of a video (through REST API form), list of questions and answers, user stats
# What are the endpoints to manipulate those resources (give a name to each resource), define what data is transferred between client/server
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

Notas: 
- VideoDB não pode ser apenas importado e chamar os seus métodos no proxy, é como se estivesse a implementar no Proxy, pois não satisfaz
a extensbilidade requerida. Provavelment ter-se-á que torná-la numa aplicação Flask para que assim interaja com o Proxy de forma extensível.

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
# 4) user stats,
# 5) logs (is it?)
#
# Operations that can be performed: 
# 1) new video (POST), get a video (POST), get the list of videos (GET),
# 2) new question (POST), view a question (all info regarding it) (GET), list of questions (GET),
# 3) new answer (POST), view a answer (is necessary?) (GET), list of answers (GET),
# 4) 
#            
# (URI and Possible Methods, GET,POST,PATCH/PUT)

from flask import Flask, abort, request, redirect, url_for, session, jsonify, render_template
from flask_dance.consumer import OAuth2ConsumerBlueprint
from time import sleep
import requests
from datetime import datetime
# import os  # necessary so that our server does not need https
# from Video_DB import *

# os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
# app.secret_key = "supersekrit"  # Replace this with your own secret!
# app.config['SESSION_TYPE'] = 'filesystem'
# app.config['SESSION_PERMANENT'] = False
# fenix_blueprint = OAuth2ConsumerBlueprint(
#     "fenix-example", __name__,
#     # this value should be retrived from the FENIX OAuth page
#     client_id="1132965128044779",
#     # this value should be retrived from the FENIX OAuth page
#     client_secret="HOmZwGuoFApLQEdqum3DTdSMk6XpLux6qJoqhZZVrKRQ+0cqo/rBnAupdik01GLsqunxF2EIR2jYef8skOS3Jg==",
#     # do not change next lines
#     base_url="https://fenix.tecnico.ulisboa.pt/",
#     token_url="https://fenix.tecnico.ulisboa.pt/oauth/access_token",
#     authorization_url="https://fenix.tecnico.ulisboa.pt/oauth/userdialog",
# )

# app.register_blueprint(fenix_blueprint)





# A log file that will store all events ocurred in the system
with open(log.txt,'w') as log:
    log.write('TIMESTAMP | EVENT\n\n')


#                           PROXY ENDPOINTS
#-----------------------------------------------------------------------------
# Related to videos

# get a list of videos
@app.route("/API/videos/", methods=['GET'])
def returnsVideosJSON():
    with open(log.txt, "a") as log:
        # datetime object containing current date and time and converting it to a string
        now = datetime.now()       
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print("date and time = ", dt_string)	
        # log.write(dt_string + ' | ' + 'Videos dictionary returned' + str(listVideosDICT()) + '\n')

    # return {"videos": listVideosDICT()}
    pass

# get a single video
@app.route("/API/videos/<int:id>/")
def returnSingleVideoJSON(id):
    # try:
    #     v = getVideoDICT(id)
    #     return v
    # except:
    #     abort(404)
    pass

# create a new video
@app.route("/API/videos/", methods=['POST'])
def createNewVideo():
    # sleep(0.1)
    # j = request.get_json()
    # print (type(j))
    # ret = False
    # try:
    #     print(j["description"])
    #     ret = newVideo(j["description"], j['url'])
    # except:
    #     abort(400)
    #     #the arguments were incorrect
    # if ret:
    #     return {"id": ret}
    # else:
    #     abort(409)
    # #if there is an erro return ERROR 409
    pass

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

# @app.route("/")
# def index():
#     return app.send_static_file('index.html')
    
# Related to users
#-----------------------------------------------------------------------------
# Related to authentication 

# @app.route('/')
# def home_page():
#     # The access token is generated everytime the user authenticates into FENIX
#     print(fenix_blueprint.session.authorized)
#     print("Access token: "+ str(fenix_blueprint.session.access_token))
#     return render_template("appPage.html", loggedIn = fenix_blueprint.session.authorized)

# @app.route('/logout')
# def logout():
#     print('Logged out!')
#     # this clears all server information about the access token of this connection
#     res = str(session.items())
#     print(res)
#     session.clear()
#     res = str(session.items())
#     print(res)
#     # when the browser is redirected to home page it is not logged in anymore
#     return redirect(url_for("home_page"))

# @app.route('/private')
# def private_page():
#     #this page can only be accessed by a authenticated user

#     # verification of the user is  logged in
#     if fenix_blueprint.session.authorized == False:
#         #if not logged in browser is redirected to login page (in this case FENIX handled the login)
#         return redirect(url_for("fenix-example.login"))
#     else:
#         #if the user is authenticated then a request to FENIX is made
#         resp = fenix_blueprint.session.get("/api/fenix/v1/person/")
#         #res contains the responde made to /api/fenix/vi/person (information about current user)
#         data = resp.json() 
#         print(resp.json())
#         return render_template("privPage.html", username=data['username'], name=data['name'])

if __name__ == "__main__":
   app.run(debug=True) # by default it will run in 127.0.0.1:5000
