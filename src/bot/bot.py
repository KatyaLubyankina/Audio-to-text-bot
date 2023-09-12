import json

import requests
import telebot
import validators
from requests import Response

import src.config as config
from src.rabbitmq.mongo import get_document_mongo

BOT_TOKEN = config.get_settings().bot_token.get_secret_value()
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start", "hello"])
def send_welcome(message) -> None:
    """Function to send hello message to user.

    Bot reacts to /start and /hello command in telegram chat.
    """
    bot.reply_to(
        message,
        "Hello! Here you can send a link to audio file to get its transcription. \
        Use /sendlink command",
    )


@bot.message_handler(commands=["sendlink"])
def get_link(message) -> None:
    """Function to process /sendlink command.

    Bot replies to user message and calls verify_link function.
    """
    msg = bot.reply_to(message, "Send a link to get transcription!")
    bot.register_next_step_handler(msg, verify_link)


def verify_link(msg) -> None:
    """Verifies link in message from user to bot.

    Args:
        msg (Message object): message in telegram bot

    Function uses validators library to validate url.
    If it's valid, function calls send_link_to_api function.
    If status code is not 200, bot sends message "Your link is invalid"
    If link is invalid, bot sends response status code.

    """
    link = msg.text
    if validators.url(link):
        text = "Started converting your link to text..."
        bot.send_message(msg.chat.id, text)
        response = send_link_to_api(msg)
        if response.status_code != 200:
            bot.send_message(msg.chat.id, response.status_code)
    else:
        bot.send_message(msg.chat.id, "Your link is invalid.")


def send_link_to_api(msg) -> Response:
    """Function to make request to API.

    Args:
        msg (Message Object): message in telegram chat

    Function sends request to fastapi endpoint "/link" with chat id and message.
    Returns:
        response: response to post request
    """
    url = config.get_settings().url_app + "/link"
    data = json.dumps({"chat_id": msg.chat.id, "link": msg.text})
    response = requests.post(url, data=data)
    return response


def send_analytic(chat_id: int, file_uuid: str) -> None:
    """Function sends analytics for video.

    Gets transcript from MongoDB with provided uuid, encode text and
    send to user in telegram chat.
    Args:
        chat_id (int): id of telegram chat
        path_to_analytics (str): path to file with analytics

    Function sends user file with analytics in chat with provided chat_id.
    """
    document = get_document_mongo(file_uuid)["transcript"]
    byte_document = document.encode("ascii")
    bot.send_document(chat_id, byte_document)


if __name__ == "__main__":
    bot.infinity_polling()
