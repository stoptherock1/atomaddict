#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, url_for


app = Flask(__name__)


@app.route('/')
def index():
    # TODO If user is logged in render index.html. Landing page otherwise.
    return render_template('index.html')


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


if __name__ == '__main__':
    app.run()
