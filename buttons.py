from pyrogram.types import KeyboardButton, ReplyKeyboardMarkup
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import emoji

btn_info = KeyboardButton(f'{emoji.INFORMATION} Info')
btn_games = KeyboardButton(f'{emoji.VIDEO_GAME} Games')
btn_fgame = KeyboardButton(f'Камень ножницы бумага')
btn_rock = KeyboardButton(f'{emoji.ROCK} Камень')
btn_scissors = KeyboardButton(f'{emoji.SCISSORS} Ножницы')
btn_paper = KeyboardButton (f'{emoji.NOTEBOOK} Бумага')
btn_quest = KeyboardButton(f'Квест')
btn_back = KeyboardButton(f'Назад')
btn_generate = KeyboardButton(f'Сгенерировать изображение')
btn_number = KeyboardButton(f'Угадай число')
inline_kb_start_quest = InlineKeyboardMarkup([
        [InlineKeyboardButton('Пройти квест',
                             callback_data='start_quest')]
    ])
inline_kb_choose_door = InlineKeyboardMarkup([
        [InlineKeyboardButton('Левая дверь', callback_data='left_door')],
        [InlineKeyboardButton('Правая дверь', callback_data='right_door')]
    ])
inline_kb_left_door = InlineKeyboardMarkup([
        [InlineKeyboardButton('Открыть', callback_data='open_it')],
        [InlineKeyboardButton('Не открывать', callback_data='close_it')]
    ])
inline_kb_right_door = InlineKeyboardMarkup([
        [InlineKeyboardButton('Сьесть', callback_data='eat_it')],
        [InlineKeyboardButton('Не трогать', callback_data='leave_it')]
    ])


kb_main = ReplyKeyboardMarkup(
    keyboard=[
        [btn_info, btn_games],
        [btn_generate]
    ],
    resize_keyboard=True
)
games = ReplyKeyboardMarkup(
    keyboard=[
        [btn_fgame],
        [btn_quest, btn_back,btn_number]
    ],
    resize_keyboard=True
)
kb_knb = ReplyKeyboardMarkup(
    keyboard=[
        [btn_rock],[btn_scissors],
        [btn_paper],[btn_back]
    ],
    resize_keyboard=True
)