#!/usr/bin/env python
#-*- coding:utf-8 -*-
#@Time : 16/8/5 下午1:09
#@Author:Powerfoo
#@File:form.py
from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_pagedown.fields import PageDownField


class EditProfileForm(Form):
    name = StringField('昵称', validators=[Length(0, 64)])
    location = StringField('住址', validators=[Length(0, 64)])
    signature = TextAreaField('个性签名')
    submit = SubmitField('Submit')


class PostForm(Form):
    body = PageDownField('整点啥', validators=[DataRequired()])
    submit = SubmitField('发表')


class CommentForm(Form):
    body = StringField('Enter your comment', validators=[DataRequired()])
    submit = SubmitField('Submit')