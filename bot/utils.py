from telegram import ReplyKeyboardMarkup


def get_keyboard():
    my_keyboard = ReplyKeyboardMarkup(
        [
            ['Добавить операцию', 'Показать последние операции'],
        ], resize_keyboard=True)
    return my_keyboard
