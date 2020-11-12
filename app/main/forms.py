from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User
from flask import request



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

class EmptyForm(FlaskForm):
    submit = SubmitField(label='提交')

class PostForm(FlaskForm):
    post = TextAreaField(label='说点什么',validators=[DataRequired()])
    submit = SubmitField(label='发布')

class SearchForm(FlaskForm):
    q = StringField(label='搜索', validators=[DataRequired()])
    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)


class MessageForm(FlaskForm):
    message = TextAreaField(label='消息', validators=[
        DataRequired(), Length(min=1,max=140)
    ])
    submit = SubmitField('发送')
