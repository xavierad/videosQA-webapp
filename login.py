from flask import Flask
from flask_dance.consumer import OAuth2ConsumerBlueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import jsonify, url_for
from flask import session
from admin.admin import construct_admin_bp
from regular.regular import construct_regular_bp


import requests


#necessary so that our server does not need https
import os
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

app.register_blueprint(fenix_blueprint)
app.register_blueprint(construct_admin_bp(fenix_blueprint), url_prefix="/admin")
app.register_blueprint(construct_regular_bp(fenix_blueprint), url_prefix="/regular")

@app.route('/')
def home_page():
    # The access token is generated everytime the user authenticates into FENIX
    print(fenix_blueprint.session.authorized)
    print("Access token: "+ str(fenix_blueprint.session.access_token))
    return render_template("appPage.html", loggedIn = fenix_blueprint.session.authorized)

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

# @app.route('/admin')
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
#         return render_template("adminPage.html", username=data['username'], name=data['name'])



if __name__ == '__main__':
    app.run(debug=True)