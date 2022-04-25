from flask import session, redirect, url_for, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash
from app.controllers.pages import home_controller, logout_controller, sign_up_controller, sign_in_controller, view_db_controller, rule_controller, account_controller
from . import main

#Home page
@main.route('/')
def home():
    return home_controller.home()

#Sign-out page
@main.route('/sign-out')
def logout():
    return logout_controller.logout()

    
#Sign-in page
@main.route('/sign-in',  methods=['GET', 'POST'])
def sign_in():
    data = None
    if(request.method == 'POST'):
        data = request.form
    return sign_in_controller.sign_in(data)

    
#Sign-up page
@main.route('/sign-up',  methods=['GET', 'POST'])
def sign_up():
    data = None
    if(request.method == 'POST'):
        data = request.form
    return sign_up_controller.sign_up(data)

    

@main.route('/view_db')
def view_db():
    return view_db_controller.test()

    
#Rule page
@main.route('/rule')
def rule():
    return rule_controller.rule()

#Account page
@main.route('/account')
def account():
    return account_controller.account()