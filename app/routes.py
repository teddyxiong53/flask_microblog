from app import app
from flask import render_template
import flask_wtf
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

