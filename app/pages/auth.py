from flask import session, Blueprint, request, redirect, render_template
from ..model.account import check_login


auth_pages = Blueprint("auth", __name__)

@auth_pages.route("/login", methods=["GET", "POST"])
def login_page():
    error = ""
    if "email" in request.form:
        email = request.form["email"]
        password = request.form["password"]
        if check_login(email, password):
            session["email"] = email
            session["auth"] = True
            return redirect("/", code=302)
        else:
            error = "Invalid username or password"
    return render_template("login.html", error=error)

@auth_pages.route("/logout")
def logout():
    session["auth"] = False
    return redirect("/")

