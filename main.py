import logging
import os
import sys

import requests
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, Updater)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv()
TG_TOKEN = os.getenv('TG_TOKEN')
API_KEY = os.getenv('api_key')
mode = os.getenv("MODE")
if mode == "dev":
    def run(updater):
        updater.start_polling()
elif mode == "prod":
    def run(updater):
        PORT = int(os.environ.get("PORT", "8443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        updater.start_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=TG_TOKEN,
            webhook_url=f'https://{HEROKU_APP_NAME}.herokuapp.com/{TG_TOKEN}')
        updater.idle()
else:
    logger.error("No MODE specified!")
    sys.exit(1)

URL = 'https://api.thecatapi.com/v1/images/search'
headers = {
    'Content-Type': 'application/json',
    'x-api-key': API_KEY,
}


def get_cat(mimetype='jpg') -> str:
    """
    Выдает ссылку на рандомного котика
    """
    params = {
        'mime_types': mimetype
    }
    response = requests.request("GET", URL, headers=headers, params=params).json()
    random_cat_url = response[0].get('url')
    return random_cat_url


def send_cat(update, context):
    """
    Отправляет сообщение с котиком
    """
    chat = update.effective_chat
    cat = get_cat()
    context.bot.send_photo(chat_id=chat.id, photo=cat)


def wake_up(update, context):
    """
    Обработка команды /start
    """
    chat = update.effective_chat
    keyboard = [
        [
            InlineKeyboardButton("Хочу котика", callback_data='jpg'),
            InlineKeyboardButton("Хочу гифку", callback_data='gif'),

        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = 'everyday is a Caturday \n' \
           'Just type /cat or click on button for new cat'
    context.bot.send_message(
        chat_id=chat.id,
        text=text,
        reply_markup=reply_markup
    )


def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    chat = update.effective_chat
    keyboard = [
        [
            InlineKeyboardButton("Хочу котика", callback_data='jpg'),
            InlineKeyboardButton("Хочу гифку", callback_data='gif'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    cat = get_cat(mimetype=query.data)
    if query.data == 'jpg':
        context.bot.send_photo(
            chat_id=chat.id,
            photo=cat,
            reply_markup=reply_markup)
    elif query.data == 'gif':
        context.bot.send_animation(
            chat_id=chat.id,
            animation=cat,
            reply_markup=reply_markup)


def main():
    updater = Updater(token=TG_TOKEN)
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('cat', send_cat))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    run(updater)


if __name__ == '__main__':
    main()
