from flask import session, redirect, url_for, render_template, request

from app.controllers.pages import home_controller, login_controller, logout_controller, pong_controller, sign_up_controller, tes_controller, view_db_controller, rule_controller
from . import main


@main.route('/')
def index():
    return home_controller.index()

# Scoreboard
@main.route('/home')
def home():
    return home_controller.home()

@main.route('/login',  methods=['GET', 'POST'])
def login():
    data = None
    if(request.method == 'POST'):
        data = request.form

    return login_controller.login(data)

@main.route('/sign-out')
def logout():
    return logout_controller.logout()

@main.route('/sign-up',  methods=['GET', 'POST'])
def sign_up():
    data = None
    if(request.method == 'POST'):
        data = request.form
    return sign_up_controller.sign_up(data)

@main.route('/view_db')
def view_db():
    return view_db_controller.test()

@main.route('/pong')
def pong():
    return pong_controller.pong()

@main.route('/test')
def test():
    return tes_controller.test()

@main.route('/rule')
def rule():
    return rule_controller.rule()


