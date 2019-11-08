import requests
from datetime import datetime
from cfg.bot_settings import WEB_API_URL
from telegram import ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import ConversationHandler
from utils import get_keyboard, get_user_default_acc, get_categories_list


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
    return "default_account"


def operation_name(update, context):
    # context.user_data['current_operation'] = {"name": str(update.message.text)}
    # update.message.reply_text("Выбор счета")
    # return "default_account"
    pass


def operation_default_account(update, context):
    # получаем имя операции
    context.user_data['current_operation'] = {"name": str(update.message.text)}

    default_account = get_user_default_acc("secretkey")
    update.message.reply_text(f"""Выбран счет по умолчанию: {default_account[1]}
Введите категорию операции, чтобы продолжить""")
    context.user_data['current_operation']['account_id'] = int(default_account[0])
    return "category"


def operation_custom_account(update, context):
    update.message.reply_text("Выберите счет из списка:")


def operation_account_button(update, context):
    query = update.callback_query
    # print(query)
    context.user_data['current_operation']['account_id'] = int(query.data)
    query.edit_message_text(text="Выбран счет: {}".format(query.data))
    return "category"


def operation_category(update, context):
    user_category = str(update.message.text)
    category_list = get_categories_list("secretkey")
    for category in category_list:
        if str(category[1]).lower() == user_category.lower():
            context.user_data['current_operation']['category_id'] = int(category[0])
            update.message.reply_text(f"Выбрана категория {category[1]}, введите сумму операции")
            return "value"
    update.message.reply_text("Категория не найдена, попробуйте еще раз")
    return "category"


def operation_value(update, context):
    try:
        operation_value = int(update.message.text)
        context.user_data['current_operation']['value'] = operation_value
        print(context.user_data)
    except ValueError:
        update.message.reply_text("Сумма введена неверно, нужно ввести только число")
        return "value"
    update.message.reply_text("Операция успешно добавлена", reply_markup=get_keyboard())
    return ConversationHandler.END


def operation_cancel(update, context):
    update.message.reply_text("Ввод отменен", reply_markup=get_keyboard())
    return ConversationHandler.END



# def operarion_tags(update, context):
#     pass


# def operarion_date(update, context):
#     pass

"""
Вводим название операции

Получить список счетов
Написать сообщение, что выбран счет № и его название
 + нажмите /change_account, если пользователь хочет поменять счет, выводим список счетов и выбираем из него
Выбрать счет

Получить список категорий
Попросить пользователя ввести название категории
    Если такая категория существует - продолжаем
    Если нет, выводим подсказку со списком доступных категорий
Выбрать категорию

Спрашивает сумму



"""
