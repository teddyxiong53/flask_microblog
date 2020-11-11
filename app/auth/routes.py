from app import  db, get_locale
from flask import render_template
from flask import flash, redirect, url_for, request, g, jsonify
from app.auth.forms import  LoginForm, RegistrationForm,\
    ResetPasswordForm, ResetPasswordRequestForm
from flask_login import current_user, login_user
from app.models import User, Post
from flask_login import logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime
from app.auth.email import send_password_reset_email
from guess_language import guess_language
from app.translate import translate
from app.auth import bp


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('用户名或者密码不对')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')

        return redirect(next_page)
    return render_template('login.html', title='登陆', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('恭喜你，注册成功')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='注册', form=form)

@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    # 登陆状态不允许
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('邮件已经发送到你的邮箱，请检查你的邮箱')
        return redirect(url_for('auth.login'))
    return render_template('reset_password_request.html',
                           title='重置密码', form=form)

@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('密码重置成功')
        return redirect(url_for('auth.login'))
    return render_template('reset_password.html', form=form)
