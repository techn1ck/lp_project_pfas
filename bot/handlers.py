from utils import get_keyboard


def unknown(update, context):
    update.message.reply_text('unknown command')


def get_started(update, context):
    update.message.reply_text('Hi!', reply_markup=get_keyboard())


def my_categories(update, context):
    pass


def my_tags(update, context):
    pass
