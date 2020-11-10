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

class EditProfileForm(FlaskForm):
    username = StringField(label="用户名", validators=[DataRequired()])
    about_me = TextAreaField(label="关于我", validators=[Length(min=0, max=1024)])
    submit = SubmitField('提交')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('该名字已经被占用了')
