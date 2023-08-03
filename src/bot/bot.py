import telebot
import src.config as config
import validators

BOT_TOKEN = config.get_settings().BOT_TOKEN.get_secret_value()
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Here you can send a link to audio file to get its transcription. Use sendlink command")


@bot.message_handler(commands=['sendlink'])
def get_link(message):
    msg = bot.reply_to(message, "Send a link to get transcription!")
    bot.register_next_step_handler(msg, check_link)

def check_link(msg):
    link = msg.text
    if validators.url(link):
        text = 'Started converting your link to text...'
        bot.send_message(msg.chat.id, text)
        bot.register_next_step_handler(msg, get_transcription)
    else:
        bot.send_message(msg.chat.id, "Your link is invalid.")
    
def get_transcription(msg):
    pass


bot.infinity_polling()