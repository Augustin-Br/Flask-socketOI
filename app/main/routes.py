from flask import session, redirect, url_for, render_template, request

from app.controllers.pages import home_controller, logout_controller, sign_up_controller, sign_in_controller, view_db_controller, rule_controller
from . import main

@main.route('/home')
def home():
    return home_controller.home()

@main.route('/sign-out')
def logout():
    return logout_controller.logout()


@main.route('/sign-in',  methods=['GET', 'POST'])
def sign_in():
    data = None
    if(request.method == 'POST'):
        data = request.form
    return sign_in_controller.sign_in(data)


@main.route('/sign-up',  methods=['GET', 'POST'])
def sign_up():
    data = None
    if(request.method == 'POST'):
        data = request.form
    return sign_up_controller.sign_up(data)


@main.route('/view_db')
def view_db():
    return view_db_controller.test()


@main.route('/rule')
def rule():
    return rule_controller.rule()
