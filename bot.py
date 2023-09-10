from telebot import telebot as tb
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from scripts.getStats import *
import settings
from datetime import datetime
import schedule
import time
import threading

bot = tb.TeleBot(settings.bot_token)
bot.set_my_commands(
    [
        tb.types.BotCommand("/ah", "main menu"),
    ])

def bot_polling_thread():
    bot.infinity_polling()
    
def scheduler_thread():
    while True:
        schedule.run_pending()
        time.sleep(1)


def anounceMarkup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("GitHub", url="https://github.com/okamietovolk/weekly_stats_bot"))
    return markup

def shitPost():
    bot.send_message(settings.public, 'penis')
    print('shitposted')



def postStats(channel = 'main'):
    bot.send_message(settings.channel(type=channel), getStats(), parse_mode="HTML", reply_markup=anounceMarkup(), disable_web_page_preview=True)

postStats()

def remind_health():
    bot.send_message(settings.admin, 'Отправь файл с экспортом здоровья. Если что это команда /ah')

@bot.message_handler(commands=["ah"])
def cfgrf(message):
    bot.send_message(message.chat.id, 'Отправь файл')

@bot.message_handler(commands=["test"])
def postTest(message):
    bot.send_message(message.chat.id, 'Щитпостим в тестовый канал')
    postStats('test')

@bot.message_handler(content_types=['document'])
def second_step(message):
    try:
        file_name = message.document.file_name
        file_id = message.document.file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Save the file
        with open(f'data/{file_name}', 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.send_message(message.chat.id, f"Received file: {file_name}")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")
    
    
schedule.every().sunday.at('22:00', 'Asia/Novosibirsk').do(postStats)
schedule.every().sunday.at('21:00', 'Asia/Novosibirsk').do(remind_health)

bot_thread = threading.Thread(target=bot_polling_thread)
scheduler_thread = threading.Thread(target=scheduler_thread)

bot_thread.start()
scheduler_thread.start()