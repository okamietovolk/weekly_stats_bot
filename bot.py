from telebot import telebot as tb
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from scripts.getStats import *
import settings
from datetime import datetime

bot = tb.TeleBot(settings.bot_token)
def anounceMarkup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("GitHub", url="https://github.com/okamietovolk/weekly_stats_bot"))
    return markup
    
bot.send_message(settings.channel('test'), getStats(), parse_mode="HTML", reply_markup=anounceMarkup(), disable_web_page_preview=True)
