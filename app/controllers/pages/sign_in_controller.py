from flask import render_template, session, redirect
from flask_socketio import SocketIO, emit
from app.controllers.auth import auth_controller
from app.models.Users import users, password_verif, encrypt_password
from ... import socketio
from ... import db
import bcrypt


def sign_in(data):


    # user haven't session
    if not session.get("username"):

        print("l'utilisateur n'a pas de session")

        # user login request
        if(data != None):
            # received login data
            print("l'utilisateur envoie les données d'authentification")

            username = data['username']
            password = data['password']
            

            # stock data into user's session

            session['username'] = username
            session['password'] = password

            print("username : ", session.get("username"))
            print("password : ", session.get("password"))

            #verify session
            
            exists = db.session.query(users._id).filter_by(name=session['username']).scalar() is not None
            
            if exists == True:
                print('l\'utilisateur existe')
                name_id = users.query.filter_by(name=session['username']).first()
                print(name_id.password)
                
                # if password == name_id.password:
                    # print('accès autorisé')
                    # return redirect('/home')
                
                verify_password = password_verif(session.get("password"), name_id.password)
                print(verify_password)
                
                if verify_password == 'True':
                    print('accès autorisé')
                    return redirect('/home')
                    
                else:
                    return redirect('/sign-up')
                         
            else:
                # l'utilisateur n'existe pas
                print('l\'utilisateur n\'existe pas')
                return redirect("/sign-up")
    

        else:
            print("l'utilisateur veux se connecté")

            navbar = auth_controller.auth()
            content =  render_template('pages/sign_in_page.html')

            return render_template("template.html", navbar = navbar, content = content, title = "Connexion")

    else:
        # user have session

        print("l'utilisateur se déconnecte")
        return redirect("/sign-out")

