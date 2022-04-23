from flask import render_template
from app.controllers.auth import auth_controller


def sign_in():
    navbar = auth_controller.auth()
    content = render_template("pages/sign_in_page.html")

    return render_template("template.html", navbar = navbar, content=content, title = "Connexion")