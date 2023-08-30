from telebot import telebot as tb
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from scripts.getStats import *
import settings
from datetime import datetime

bot = tb.TeleBot(settings.bot_token)
def anounceMarkup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("GitHub", url="t.me/weristvlad"))
    return markup
    

bot.send_message(settings.publish_chat, getStats(), parse_mode="HTML", reply_markup=anounceMarkup())
