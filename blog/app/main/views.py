#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 16/8/4 上午11:09
# @Author:Powerfoo
# @File:views.py
from flask import render_template, redirect, url_for, request, abort, make_response, current_app
from . import main
from ..model import User, Post, Comment
from .form import EditProfileForm, PostForm, CommentForm
from flask_login import login_required
from .. import db
from flask_login import current_user


@main.route('/')
def homepage():
    return render_template('homepage.html', title='主页')


@main.route('/practical_knowledge')
def knowledge():
    return render_template('knowledge.html', title='名家荟萃')


@main.route('/soul_soup')
def soup():
    return render_template('soup.html', title='心灵鸡汤')


@main.route('/community', methods=['GET', 'POST'])
def community():
    page = request.args.get('page', 1, type=int)
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.community'))
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query
    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page, error_out=False)
    posts = pagination.items
    return render_template('community.html',
                           title='七嘴八舌', form=form, posts=posts,
                           show_followed=show_followed, pagination=pagination)


@main.route('/about_me')
def about():
    return render_template('about.html', title='关于作者')


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, title='个人信息', posts=posts)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.signature = form.signature.data
        db.session.add(current_user)
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.signature.data = current_user.signature
    return render_template('edit_profile.html', form=form, title='填写个人资料')


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        return redirect(url_for('.post', id=post.id))
    page = request.args.get('page', 1, type=int)
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form,
                           comments=comments, pagination=pagination)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        return redirect(url_for('.post', id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)


@main.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return redirect(url_for('.homepage'))
    if current_user.is_following(user):
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    return redirect(url_for('.user', username=username))


@main.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return redirect(url_for('.homepage'))
    if not current_user.is_following(user):
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    return redirect(url_for('.user', username=username))


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return redirect(url_for('.homepage'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followers of",
                           endpoint='.followers', pagination=pagination,
                           follows=follows)


@main.route('/followed-by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return redirect(url_for('.homepage'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followed by",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)


@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.community')))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    return resp


@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.community')))
    resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
    return resp
