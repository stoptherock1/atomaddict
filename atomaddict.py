#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, url_for
from database.session import Get

app = Flask(__name__)


@app.route('/')
def index():
    # TODO If user is logged in render index.html. Ladning page otherwise.
    get = Get()
    user = get.all_users()[0]
    print user
    tags = []
    if user:
        for tag in user.tags:
            tags.append(tag)
    print tags
    get.close_session()
    return render_template('index.html',
                           user=user,
                           tags=tags)


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


@app.route('/base')
def base():
    return render_template('base.html')


if __name__ == '__main__':
    app.run()
