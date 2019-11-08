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
from bot.operation_handlers import my_operations, operation_add, operation_value, operation_category, operation_cancel, operation_default_account

locale.setlocale(locale.LC_ALL, "ru_RU")
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )
logger = logging.getLogger(__name__)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(TELEGRAM_API_KEY, request_kwargs=PROXY, use_context=True)
    dp = updater.dispatcher

    new_operation = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^(Добавить операцию)$'), operation_add)],
        states={
            "default_account": [MessageHandler(Filters.text, operation_default_account)],
            "category": [MessageHandler(Filters.text, operation_category)],
            "value": [MessageHandler(Filters.text, operation_value)],
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
