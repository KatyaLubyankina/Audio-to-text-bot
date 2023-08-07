import json

import requests
import telebot
import validators

import src.config as config

BOT_TOKEN = config.get_settings().BOT_TOKEN.get_secret_value()
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start", "hello"])
def send_welcome(message):
    bot.reply_to(
        message,
        "Hello! Here you can send a link to audio file to get its transcription. \
        Use /sendlink command",
    )


@bot.message_handler(commands=["sendlink"])
def get_link(message):
    msg = bot.reply_to(message, "Send a link to get transcription!")
    bot.register_next_step_handler(msg, handel_client)


def handel_client(msg):
    link = msg.text
    if validators.url(link):
        text = "Started converting your link to text..."
        bot.send_message(msg.chat.id, text)
        response = handel_api(msg)
        if response.status_code == 200:
            bot.send_message(msg.chat.id, response.json()["response"])
        else:
            bot.send_message(msg.chat.id, response.status_code)
    else:
        bot.send_message(msg.chat.id, "Your link is invalid.")


def handel_api(msg):
    url = config.get_settings().url_to_sent_link
    data = json.dumps({"chat_id": msg.chat.id, "link": msg.text})
    response = requests.post(url, data=data)
    return response


bot.infinity_polling()
