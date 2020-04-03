from flask import Flask, request
import telegram
import time
from telebot.credentials import bot_token, bot_user_name,URL
from telebot import covid


global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()
    # for debugging purposes only
    print("got text message :", text)
    # the first time you chat with the bot AKA the welcoming message
    if text == "/start":
        # print the welcoming message
        bot_welcome = """
       \nWelcome to CoronaCounter bot,\nSend the name of the country yo bot whose information you would like to find out stay updated!\n\nType   #<country_name>  for more details of that country.\n\nPlease type  "total" or "#total" for world's status\n\n
       """
        # send the welcoming message
        bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)


    else:

        message = text
        try:
            if (message[0] == '#'):
                reply = covid.all_info(message)
            else:
                reply = covid.total_cases(message)
            bot.sendMessage(chat_id=chat_id, text=reply, reply_to_message_id=msg_id)
        except Exception:
            # if things went wrong
            bot.sendMessage(chat_id=chat_id, text="We are encountering server issues right now. We will be back soon. Thank you for your patience. ", reply_to_message_id=msg_id)

    return 'ok'

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route('/')
def index():
    return '.'


if __name__ == '__main__':
    app.run(threaded=True)