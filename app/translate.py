import json
import requests
from flask_babel import _
from app import app

def translate(text, src, dst):
    if 'MS_TRANLATOR_KEY' not in app.config or not app.config['MS_TRANSLATOR_KEY']:
        return '翻译服务没有配置'
    auth = {
        'Ocp-Apim-Subscription-Key': app.config['MS_TRANSLATOR_KEY']
    }
    r = requests.get('https://api.microsofttranslator.com/v2/Ajax.svc/Translate?text={}&from={}&to={}'.format(
        text, src,dst
    ), headers=auth)
    if r.status_code != 200:
        return '翻译服务失败了'
    return json.loads(r.content.decode('utf-8-sig'))

