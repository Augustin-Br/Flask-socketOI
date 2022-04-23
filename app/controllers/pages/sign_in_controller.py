from flask import render_template, session, redirect
from app.controllers.auth import auth_controller


def sign_in(data):


    # user haven't session
    if not session.get("username"):

        print("l'utilisateur n'a pas de session")

        # user login request
        if(data != None):
            # received login data
            print("l'utilisateur envoie les données d'authentification")

            username = data['username']

            # stock data into user's session

            session['username'] = username

            print("user name : ", session.get("username"))

            # redirection user to home page

            return redirect("/home")

        else:
            print("l'utilisateur veux se connecté")

            navbar = auth_controller.auth()
            content =  render_template('pages/sign_in_page.html')

            return render_template("template.html", navbar = navbar, content = content, title = "Connexion")

    else:
        # user have session

        print("l'utilisateur se déconnecte")
        return redirect("/sign-out")

