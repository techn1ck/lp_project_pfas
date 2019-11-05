import requests
from datetime import datetime
from cfg.bot_settings import WEB_API_URL
from telegram import ParseMode
from telegram import ReplyKeyboardRemove

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


def operarion_add(update, context):
    user_text = "Выберите счет: "
    update.message.reply_text(user_text, reply_markup=ReplyKeyboardRemove())


def operarion_account(update, context):
    pass


def operarion_category(update, context):
    pass


def operarion_name(update, context):
    pass


def operarion_value(update, context):
    pass


def operarion_tags(update, context):
    pass


def operarion_date(update, context):
    pass
"""

Получить список счетов
Вывести в виде инлайн клавиатуры
Выбрать счет

Получить список категорий
Вывести в виде инлайн клавиатуры
Выбрать категорию

Спрашивает имя операции
Спрашивает сумму

Теги?

Дата
	Ввести дату (инлайн клавиатура) если отличается от текущей (пока не делаю)

"""