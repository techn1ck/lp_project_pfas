import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

import locale
import logging
import traceback
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram.utils.helpers import mention_html

from cfg.bot_settings import TELEGRAM_API_KEY, PROXY
from bot.handlers import get_started, my_categories, my_tags, unknown
from bot.operation_handlers import my_operations, operation_add, operation_name, operation_value, operation_account, operation_category, operation_account_button, operation_cancel

locale.setlocale(locale.LC_ALL, "russian")
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )
logger = logging.getLogger(__name__)


# this is a general error handler function. If you need more information about specific type of update, add it to the
# payload in the respective if clause
def error(update, context):
    # add all the dev user_ids in this list. You can also add ids of channels or groups.
    devs = [170170740]
    # we want to notify the user of this problem. This will always work, but not notify users if the update is an
    # callback or inline query, or a poll update. In case you want this, keep in mind that sending the message
    # could fail
    if update.effective_message:
        text = "Hey. I'm sorry to inform you that an error happened while I tried to handle your update. " \
               "My developer(s) will be notified."
        update.effective_message.reply_text(text)
    # This traceback is created with accessing the traceback object from the sys.exc_info, which is returned as the
    # third value of the returned tuple. Then we use the traceback.format_tb to get the traceback as a string, which
    # for a weird reason separates the line breaks in a list, but keeps the linebreaks itself. So just joining an
    # empty string works fine.
    trace = "".join(traceback.format_tb(sys.exc_info()[2]))
    # lets try to get as much information from the telegram update as possible
    payload = ""
    # normally, we always have an user. If not, its either a channel or a poll update.
    if update.effective_user:
        payload += f' with the user {mention_html(update.effective_user.id, update.effective_user.first_name)}'
    # there are more situations when you don't get a chat
    if update.effective_chat:
        payload += f' within the chat <i>{update.effective_chat.title}</i>'
        if update.effective_chat.username:
            payload += f' (@{update.effective_chat.username})'
    # but only one where you have an empty payload by now: A poll (buuuh)
    if update.poll:
        payload += f' with the poll id {update.poll.id}.'
    # lets put this in a "well" formatted text
    text = f"Hey.\n The error <code>{context.error}</code> happened{payload}. The full traceback:\n\n<code>{trace}" \
           f"</code>"
    # and send it to the dev(s)
    for dev_id in devs:
        context.bot.send_message(dev_id, text, parse_mode=ParseMode.HTML)
    # we raise the error again, so the logger module catches it. If you don't use the logger module, use it.
    raise


def main():
    updater = Updater(TELEGRAM_API_KEY, request_kwargs=PROXY, use_context=True)
    dp = updater.dispatcher

    new_operation = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^(Добавить операцию)$'), operation_add)],
        states={
            "account": [MessageHandler(Filters.text, operation_account),
                        CallbackQueryHandler(operation_account_button)],
            "category": [MessageHandler(Filters.text, operation_category)],
            "name": [MessageHandler(Filters.text, operation_name)],
            # "tags": [MessageHandler(Filters.text, operation_tags)],
            # "date": [MessageHandler(Filters.text, operation_date)],
        },
        fallbacks=[MessageHandler(Filters.text | Filters.video | Filters.photo | Filters.document, unknown),
                   CommandHandler('cancel', operation_cancel)
                   ]
    )
    dp.add_handler(CommandHandler('start', get_started))
    dp.add_handler(CommandHandler('categories', my_categories))
    dp.add_handler(CommandHandler('tags', my_tags))

    dp.add_handler(MessageHandler(Filters.regex('^(Показать последние операции)$'), my_operations))
    dp.add_handler(new_operation)

    dp.add_handler(MessageHandler(Filters.command, unknown))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
