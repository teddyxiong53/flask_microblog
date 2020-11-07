from app import app
from flask import render_template
import flask_wtf
from flask import flash, redirect, url_for
from app.forms import  LoginForm

@app.route('/')
@app.route('/index')
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
    form = LoginForm()
    if form.validate_on_submit():
        flash('login request for user {}, rember me = {}'.format(
            form.username.data,
            form.remember_me.data
        ))
        return redirect(url_for('index')) # 不能写成/index。
    return render_template('login.html', title='Sign In', form=form)

