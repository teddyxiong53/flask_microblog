from app import app, db
from flask import render_template
import flask_wtf
from flask import flash, redirect, url_for, request
from app.forms import  LoginForm, RegistrationForm
from flask_login import current_user, login_user
from app.models import User
from flask_login import logout_user, login_required
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'teddy'}
    posts = [
        {
            "author": {'username':"李白"},
            "body": "床前明月光，\
                疑是地上霜。\
                举头望明月，\
                低头思故乡。"
        },
        {
            "author": {'username':"白居易"},
            "body": "离离原上草，一岁一枯荣。\
                野火烧不尽，春风吹又生。\
                远芳侵古道，晴翠接荒城。\
                又送王孙去，萋萋满别情。"
        }
    ]
    return render_template('index.html', title='home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('用户名或者密码不对')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for(index))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('恭喜你，注册成功')
        return redirect(url_for('login'))
    return render_template('register.html', title='注册', form=form)

