import os, click
from app import app

@app.cli.group()
def translate():
    pass

@translate.command()
@click.argument('lang')
def init(lang):
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command not support')
    if os.system('pybabel init -i messages.pot -d app/translations -l' + lang):
        raise RuntimeError('init command failed')
    os.remove('messages.pot')

@translate.command()
def update():
    '''
    更新所有语言
    :return:
    '''
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command not support')
    if os.system(('pybabel update -i messages.pot -d app/translations')):
        raise RuntimeError('update command fail')
    os.remove('messages.pot')

@translate.command()
def compile():
    if os.system('pybabel compile -d app/translations'):
        raise RuntimeError('compile command failed')
