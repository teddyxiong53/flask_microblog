from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
    username = StringField(label='用户名', validators=[DataRequired()])
    password = PasswordField(label='密码', validators=[DataRequired()])
    remember_me = BooleanField(label='记住我')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField(label='用户名', validators=[DataRequired()])
    email = StringField(label='邮箱', validators=[DataRequired(), Email()])
    password = PasswordField(label='密码', validators=[DataRequired()])
    password2 = PasswordField(label='再次输入密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('注册')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('用户名已经被占用了')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('邮箱已经被占用了')



class ResetPasswordRequestForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    submit = SubmitField('发送请求')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField('再次输入密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label="设置密码")
