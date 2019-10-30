import requests
import json
from cfg.bot_settings import WEB_API_URL


def unknown(update, context):
    update.message.reply_text('unknown command')


def get_started(update, context):
    update.message.reply_text('Hi!')


def my_operations(update, context):
    r = requests.post(WEB_API_URL + "secretkey/get/operations/")
    if r.status_code != "200":
        result = json.loads(r.text())
        print(result)
    else:
        update.message.reply_text('error')


def my_categories(update, context):
    pass


def my_tags(update, context):
    pass
