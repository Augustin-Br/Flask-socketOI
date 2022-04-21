from flask import session, render_template, request, redirect



def login(data):

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

            return redirect("/")

        else:
            print("l'utilisateur veux se connecté")
            return render_template('sign_in_page.html')

    else:
        # user have session

        print("l'utilisateur se déconnecte")
        return redirect("/sign-out")

