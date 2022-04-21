from flask import session, redirect, url_for, render_template, request

from app.controllers.pages import home_page, login_page, logout_page, pong_page, view_db_page, sign_up_page, test_page
from . import main


@main.route('/')
def index():
    return home_page.index()

# Scoreboard
@main.route('/home')
def home():
    return home_page.home()

@main.route('/login',  methods=['GET', 'POST'])
def login():
    data = None
    if(request.method == 'POST'):
        data = request.form

    return login_page.login(data)

@main.route('/sign-out')
def logout():
    return logout_page.logout()

@main.route('/sign-up',  methods=['GET', 'POST'])
def sign_up():
    data = None
    if(request.method == 'POST'):
        data = request.form
    return sign_up_page.sign_up(data)

@main.route('/view_db')
def view_db():
    return view_db_page.test()

@main.route('/pong')
def pong():
    return pong_page.pong()

@main.route('/test')
def test():
    return test_page.test()


