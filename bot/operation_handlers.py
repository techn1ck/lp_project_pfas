import requests
from datetime import datetime
from cfg.bot_settings import WEB_API_URL
from telegram import ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import ConversationHandler
from utils import get_user_accs, get_keyboard


def my_operations(update, context):
    r = requests.post(WEB_API_URL + "secretkey/get/operations/")
    if r.status_code == 200:
        result = r.json()
        user_text = """<b>Последние операции:</b>
"""
        for operation in result:
            try:
                date_object = datetime.strptime(operation['creation_time'], "%Y-%m-%d %H:%M:%S.%f")
            except ValueError:
                # при добавлении операции через форму, добавляются микросекунды, вручную - нет
                date_object = datetime.strptime(operation['creation_time'], "%Y-%m-%d %H:%M:%S")
            operation_time = datetime.strftime(date_object, "%Y-%m-%d в %H:%M")

            operation_text = f"""{operation_time} - {operation['name']} - {operation['value']}
"""
            user_text += operation_text
        update.message.reply_text(user_text, parse_mode=ParseMode.HTML)
    else:
        update.message.reply_text('error')


def operation_add(update, context):
    update.message.reply_text("Введите название операции либо /cancel для отмены", reply_markup=ReplyKeyboardRemove())
    return "account"


def operation_account(update, context):
    context.user_data['current_operation'] = {"name": str(update.message.text)}

    reply_markup = get_user_accs("secretkey")
    update.message.reply_text("Выберите счет:", reply_markup=reply_markup)


def operation_account_button(update, context):
    query = update.callback_query
    # print(query)
    context.user_data['current_operation']['account_id'] = int(query.data)
    query.edit_message_text(text="Выбран счет: {}".format(query.data))
    update.message.reply_text("Категория")
    return "category"


def operation_category(update, context):
    print("category")

    return "name"


def operation_name(update, context):
    return "value"


def operation_value(update, context):
    return ConversationHandler.END


def operation_cancel(update, context):
    update.message.reply_text("Ввод отменен", reply_markup=get_keyboard())
    return ConversationHandler.END



# def operarion_tags(update, context):
#     pass


# def operarion_date(update, context):
#     pass

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
