from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.web_app_info import WebAppInfo

web_app = WebAppInfo(url='https://18bezrukiy.github.io/')

def keyboard():
    kb = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn = KeyboardButton(text='Store', web_app=web_app)
    return kb.add(btn)

cb = CallbackData('btn', 'action')
key = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton('Pay', callback_data='btn:pay')]]
)