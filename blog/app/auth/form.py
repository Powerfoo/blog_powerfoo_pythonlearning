#!/usr/bin/env python
#-*- coding:utf-8 -*-
#@Time : 16/8/4 上午9:37
#@Author:Powerfoo
#@File:form.py
from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..model import User


class LoginForm(Form):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')


class RegistratiomForm(Form):
    email = StringField('邮箱地址', validators=[DataRequired(),
                                            Length(1, 64),
                                            Email()])
    username = StringField('用户名', validators=[DataRequired(),
                                              Length(1, 64),
                                              Regexp('^[A-Za-z0-9_.]*$', 0, '用户名由数字、字母、下划线组成')])
    password = PasswordField('密码', validators=[DataRequired(),
                                               EqualTo('password2')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经被注册')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')


class ChangePasswordForm(Form):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    password = PasswordField('New password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm new password', validators=[DataRequired()])
    submit = SubmitField('Update Password')