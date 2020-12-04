from flask import Flask, render_template, Blueprint, redirect, url_for


def construct_regular_bp(fenix_blueprint):
    regular = Blueprint("regular", __name__, static_folder="static", template_folder="templates")

    @regular.route("/home")
    @regular.route("/")
    def regular_page():
        #this page can only be accessed by a authenticated user

        # verification of the user is  logged in
        if fenix_blueprint.session.authorized == False:
            #if not logged in browser is redirected to login page (in this case FENIX handled the login)
            return redirect(url_for("fenix-example.login"))
        else:
            #if the user is authenticated then a request to FENIX is made
            resp = fenix_blueprint.session.get("/api/fenix/v1/person/")
            #res contains the responde made to /api/fenix/vi/person (information about current user)
            data = resp.json() 
            print(resp.json())
            return render_template("regularPage.html", username=data['username'], name=data['name'])

    @regular.route('/video_page')
    @regular.route('/video_page/<string:id>')
    def video_page(id):
        # id = int(id)
        return render_template("regular_videoPage.html", videoID=id)  


    return regular 
