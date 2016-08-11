#!/usr/bin/env python
#-*- coding:utf-8 -*-
#@Time : 16/8/4 上午11:17
#@Author:Powerfoo
#@File:manager.py
import os
from flask_script import Manager, Shell
from livereload import Server
from app import create_app, db
from app.model import User, Role, Post
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Post=Post)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def dev():
    live_server = Server(app.wsgi_app)
    live_server.watch('**/*.*')
    live_server.serve(open_url=True, restart_delay=1)

if __name__ == '__main__':
    manager.run()
