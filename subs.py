from telebot import telebot as tb
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import settings

bot = tb.TeleBot(settings.bot_token)

def spamMarkup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Подписаться на Влада", url="https://t.me/weristvlad"))
    return markup

bot.send_message(settings.channel('main'), 'Подпишитесь я не крутой и не интересный', reply_markup=spamMarkup())