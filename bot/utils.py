import requests
from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from cfg.bot_settings import WEB_API_URL


def get_keyboard():
    my_keyboard = ReplyKeyboardMarkup(
        [
            ['Добавить операцию', 'Показать последние операции'],
        ], resize_keyboard=True)
    return my_keyboard


def get_user_accs(secretkey):
    '''
    Принимает имя пользователя и секретный ключ
    Возвращает inline клавиатуру со списком счетов
    '''
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



