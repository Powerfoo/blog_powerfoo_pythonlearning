#!/usr/bin/env python
#-*- coding:utf-8 -*-
#@Time : 16/8/4 下午1:54
#@Author:Powerfoo
#@File:views.py
from flask import render_template, redirect, url_for, request, flash
from app.auth import auth
from .. import db
from ..model import User
from flask_login import login_user, logout_user, login_required, current_user
from app.auth.form import LoginForm
from app.auth.form import RegistratiomForm, ChangePasswordForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.homepage'))
        flash('无效的用户名或密码')
    return render_template('auth/login.html', title='登录', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistratiomForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('main.edit_profile'))
    return render_template('auth/register.html', title='注册',
                           form=form)
'''
@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint[:5] != 'auth.' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))
'''