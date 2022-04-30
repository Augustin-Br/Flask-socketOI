from flask import render_template
from app.controllers.auth import auth_controller


def rule():
    navbar = auth_controller.auth()


    content = render_template("pages/rule_page.html")
    
    foother = render_template("layout/foother.html")

    return render_template("template.html", title="Accueil", navbar = navbar, content = content, foother = foother)


