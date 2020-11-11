from app import app, cli
from app.models import  User, Post
from app import db

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Post': Post
    }


