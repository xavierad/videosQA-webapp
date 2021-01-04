# -------------------------------------------------------------------------------------
#                   Architectures and Internet Systems Project 2020/2021
#
# Developed by Pedro Martin (87094) & Xavier Dias (87136)
# -------------------------------------------------------------------------------------

from flask import Flask, render_template, Blueprint, redirect, url_for

def construct_admin_bp(fenix_blueprint):
    admin = Blueprint("admin", __name__, static_folder="static", template_folder="templates")

    @admin.route("/home")
    @admin.route("/")
    def admin_page():
        #this page can only be accessed by a authenticated user
        # verification of the user is  logged in
        if fenix_blueprint.session.authorized == False:
            #if not logged in browser is redirected to login page (in this case FENIX handled the login)
            return redirect(url_for("fenix-example.login"))
        try:
            #if the user is authenticated then a request to FENIX is made
            resp = fenix_blueprint.session.get("/api/fenix/v1/person/")
            #res contains the responde made to /api/fenix/vi/person (information about current user)
            data = resp.json()
            return render_template("adminPage.html", username=data['username'], name=data['name'])
        except:
            return redirect(url_for("fenix-example.login"))

    # to display the list of videos
    @admin.route('/video_page')
    @admin.route('/video_page/<string:id>')
    def video_page(id):
        # verification of the user is logged in
        if fenix_blueprint.session.authorized == False:
            #if not logged in browser is redirected to login page (in this case FENIX handled the login)
            return redirect(url_for("fenix-example.login"))
        try:
            #if the user is authenticated then a request to FENIX is made
            resp = fenix_blueprint.session.get("/api/fenix/v1/person/")
            #resp contains the response made to /api/fenix/vi/person (information about current user)
            user = resp.json()
            return render_template("admin_videoPage.html", videoID=id, username=user['username'], name=user['name'])
        except:
            return redirect(url_for("fenix-example.login"))

    # to display the video page selected from the list of videos
    @admin.route('/user_statistics')
    def user_statistics():
        try:
            #if the user is authenticated then a request to FENIX is made
            resp = fenix_blueprint.session.get("/api/fenix/v1/person/")
            #resp contains the response made to /api/fenix/vi/person (information about current user)
            user = resp.json() 
            return render_template("user_statistics.html", username=user['username'], name=user['name'])
        except:
            return redirect(url_for("fenix-example.login"))

    # to display the logs events
    @admin.route('/logs_file')
    def logs_file():
        try:
            #if the user is authenticated then a request to FENIX is made
            resp = fenix_blueprint.session.get("/api/fenix/v1/person/")
            #resp contains the response made to /api/fenix/vi/person (information about current user)
            user = resp.json() 
            return render_template("logs_list_page.html", username=user['username'], name=user['name'])
        except:
            return redirect(url_for("fenix-example.login"))

    # to get the logs file
    @admin.route('/get_and_read_file')
    def get_and_read_file():
        f = open("log.txt", "r")
        text = f.read()
        return text

    return admin 
