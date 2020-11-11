from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User



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

