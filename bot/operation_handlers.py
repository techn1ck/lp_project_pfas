import requests
from datetime import datetime
from cfg.bot_settings import WEB_API_URL
from telegram import ParseMode


def my_operations(update, context):
    r = requests.post(WEB_API_URL + "secretkey/get/operations/")
    if r.status_code != "200":
        result = r.json()
        user_text = """<b>Последние операции:</b>
"""
        for operation in result:
            date_object = datetime.strptime(operation['creation_time'], "%Y-%m-%d %H:%M:%S")
            operation_time = datetime.strftime(date_object, "%Y-%m-%d в %H:%M")

            operation_text = f"""{operation_time} - {operation['name']} - {operation['value']}
"""
            user_text += operation_text
        update.message.reply_text(user_text, parse_mode=ParseMode.HTML)
    else:
        update.message.reply_text('error')


def operarion_add():
    pass


def operarion_name():
    pass


def operarion_value():
    pass
