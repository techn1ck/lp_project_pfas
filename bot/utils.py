import requests
from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from cfg.bot_settings import WEB_API_URL


def get_keyboard():
    my_keyboard = ReplyKeyboardMarkup(
        [
            ['Добавить операцию', 'Показать последние операции'],
        ], resize_keyboard=True)
    return my_keyboard


def get_user_accs_keyboard(secretkey):
    """
    Принимает секретный ключ
    Возвращает inline клавиатуру со списком счетов пользователя
    """
    r = requests.post(WEB_API_URL + secretkey + "/get/accounts/")
    if r.status_code == 200:
        result = r.json()
        keyboard = []
        for account in result:
            account_button = [InlineKeyboardButton(account[1], callback_data=account[0])]
            keyboard.append(account_button)
        return InlineKeyboardMarkup(keyboard)
    else:
        return "error"


def get_user_default_acc(secretkey):
    r = requests.post(WEB_API_URL + secretkey + "/get/accounts/")
    if r.status_code == 200:
        result = r.json()
        # пока что выбираем просто первый из списка, в будущем можно сделать, чтобы счет по-умолчанию всегда выдавался первым, либо в api добавить такую функцию, чтобы каждый раз не гонять весь список
        default_account = result[0]
        return default_account
    else:
        return


def get_user_accs_list(secretkey):
    r = requests.post(WEB_API_URL + secretkey + "/get/accounts/")
    if r.status_code == 200:
        result = r.json()
        return result
    else:
        return


def get_user_categories(secretkey):
    r = requests.post(WEB_API_URL + secretkey + "/get/category/")
    if r.status_code == 200:
        result = r.json()
        keyboard = []
        for account in result:
            account_button = [InlineKeyboardButton(account[1], callback_data=account[0])]
            keyboard.append(account_button)
        return InlineKeyboardMarkup(keyboard)
    else:
        return "error"
