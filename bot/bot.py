import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

import locale
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from cfg.bot_settings import TELEGRAM_API_KEY, PROXY
from handlers import get_started, my_categories, my_operations, my_tags, unknown


locale.setlocale(locale.LC_ALL, "russian")
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )
logger = logging.getLogger(__name__)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(TELEGRAM_API_KEY, request_kwargs=PROXY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', get_started))

    dp.add_handler(CommandHandler('operations', my_operations))
    dp.add_handler(CommandHandler('categories', my_categories))
    dp.add_handler(CommandHandler('tags', my_tags))

    dp.add_handler(MessageHandler(Filters.command, unknown))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
