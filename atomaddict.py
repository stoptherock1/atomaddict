#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, url_for, json, session, g
from database.session import Get, set_user_tags, get_user_unreaded_articles_as_dict,\
    mark_articles_as_readed, Add, Put
from flask.globals import request
from flask_login import LoginManager, login_user
from database.model.models import User
from forms.forms import SignupForm, SigninForm
from matplotlib.backends.qt_editor import formsubplottool

app = Flask(__name__)
app.secret_key = 'temporarly secret key'
login_manager = LoginManager()


@app.route('/save_tags', methods=['GET', 'POST'])
def save_tags():

    if 'email' not in session:
        return redirect(url_for('sign_in'))
    # get user
    get = Get()
    user = get.user(email=session['email'])
    if not user:
        get.close_session()
        return redirect(url_for('sign_in'))

    tags = []
    for req in request.form:
        tags.append(req)

    # refresh user tags
    set_user_tags(email=user.email, tags=tags)

    get.close_session()
    return redirect(url_for('index'))


@app.route('/article_readed', methods=['GET', 'POST'])
def article_readed():

    if 'email' not in session:
        return redirect(url_for('sign_in'))

    article_id = request.form['article_id']

    # delete article from user
    get = Get()
    user = get.user(email=session['email'])
    get.close_session()
    if not user:
        get.close_session()
        return redirect(url_for('sign_in'))

    mark_articles_as_readed(user_email=user.email, article_id=article_id)
    return redirect(url_for('index'))


@app.route('/')
def index():
    # TODO If user is logged in render index.html. Ladning page otherwise.

    if 'email' not in session:
        return redirect(url_for('sign_in'))

    # get user
    get = Get()
    user = get.user(email=session['email'])
    if not user:
        get.close_session()
        return redirect(url_for('sign_in'))

    tags_and_articles = get_user_unreaded_articles_as_dict(email=user.email)
    tags = get.user_tags_as_dictionary(email=user.email)
    get.close_session()

    return render_template('index.html',
                           user=user,
                           tags=tags,
                           tags_and_articles=tags_and_articles)


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    form = SignupForm()
    form_in = SigninForm()

    if request.method == 'POST':
        if form.validate() is False:
            return render_template('sign.html', form_up=form,
                                   form_in=form_in,
                                   switch=True)
        else:
            put = Put()
            user = put.user(email=form.email_sign_up.data,
                            password=form.password.data,
                            nickname=form.nickname.data)
            put.close_session()
            session['email'] = user
            return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template('sign.html', form_up=form, form_in=form_in,
                               switch=True)


@app.route('/signin', methods=['GET', 'POST'])
def sign_in():
    form = SigninForm()
    form_up = SignupForm()

    if request.method == 'POST':
        if form.validate() is False:
            return render_template('sign.html', form_in=form,
                                   form_up=form_up,
                                   switch=False)
        else:
            session['email'] = form.email_sign_in.data
            return redirect(url_for('index'))

    elif request.method == 'GET':
        return render_template('sign.html', form_in=form, form_up=form_up,
                               switch=False)


@app.route('/signout')
def sign_out():
    if 'email' not in session:
        return redirect(url_for('sign_in'))

    session.pop('email', None)
    return redirect(url_for('sign_in'))


@app.route('/settings')
def settings():
    # TODO Save user's settings
    return 'Settings updated'


@app.route('/base')
def base():
    return render_template('base.html')


if __name__ == '__main__':
    app.run(debug=True)
    login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_email):
    get = Get()
    user = get.user(email=user_email)
    get.close_session()
    return user
