#!/usr/bin/env python
#-*- coding:utf-8 -*-
#@Time : 16/8/4 下午1:50
#@Author:Powerfoo
#@File:__init__.py.py
from flask import Blueprint


main = Blueprint('main', __name__)

from . import views
