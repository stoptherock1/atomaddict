#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, url_for, json
from database.session import Get
from flask.wrappers import Response, Request
from flask.globals import request

app = Flask(__name__)


@app.route('/save_tags', methods=['GET', 'POST'])
def save_tags():
    req = request.form
    print req


@app.route('/', methods=['GET', 'POST'])
def index():
    # TODO If user is logged in render index.html. Ladning page otherwise.
    get = Get()
    user = get.all_users()[0]
    (user, usertags, articles_and_tags) = \
        get.user_tags_and_articles(email=user.email)
    avaliable_tags = get.all_tags()
    print avaliable_tags
    get.close_session()

    tags = get.user_tags_as_dictionary(email=user.email)
    print tags

    return render_template('index.html',
                           user=user,
                           tags=tags,
                           usertags=usertags,
                           avaliable_tags=avaliable_tags,
                           articles_and_tags=articles_and_tags)


@app.route('/signup')
def sign_up():
    # TODO Acutall signing up
    return 'Sign up page'


@app.route('/signin')
def sign_in():
    # TODO Acutall signing in
    return 'Sign in page'


@app.route('/signout')
def sign_out():
    # TODO Acutall signing out
    return redirect(url_for('index'))


@app.route('/settings')
def settings():
    # TODO Save user's settings
    return 'Settings updated'


@app.route('/base')
def base():
    return render_template('base.html')


if __name__ == '__main__':
    app.run(debug=True)
