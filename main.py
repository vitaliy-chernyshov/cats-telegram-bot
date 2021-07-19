from dotenv import load_dotenv
import logging
import os

import requests
from telegram.ext import Updater, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv()
TG_TOKEN = os.getenv('TG_TOKEN')
API_KEY = os.getenv('api_key')
URL = 'https://api.thecatapi.com/v1/images/search'
headers = {
    'Content-Type': 'application/json',
    'x-api-key': API_KEY,
}


def get_cat_jpg() -> str:
    """
    Выдает ссылку на рандомного котика
    """
    params = {
        'mime_types': 'jpg'
    }
    response = requests.request("GET", URL, headers=headers, params=params).json()
    return response


def get_cat_url(response) -> str:
    return response[0].get('url')


def send_cat(update, context):
    """
    Отправляет сообщение с котиком
    """
    chat = update.effective_chat
    cat = get_cat_url(get_cat_jpg())
    context.bot.send_photo(chat_id=chat.id, photo=cat)


def wake_up(update, context):
    """
    Обработка команды /start
    """
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text='everyday is a Caturday.')


def main():
    updater = Updater(token=TG_TOKEN)
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('cat', send_cat))
    updater.start_polling()


if __name__ == '__main__':
    main()

