from pyrogram import Client, filters
import config
import buttons
import datetime
import random
import json
import base64
from FusionBrain_AI import generate
from pyrogram.types import ForceReply
current_date_time = datetime.datetime.now()
current_time = current_date_time.time()

bot = Client(
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    name="my_bot"
)
@bot.on_message(filters.command("image"))
async def image(bot, message):
    if len(message.text.split()) >1:
        query = message.text.replace('/image','')
        await message.reply_text(f"Генерирую изображение по запросу'{query}, подождите немного...")
        images = await generate(query)
        if images:
            image_data = base64.b64decode(images[0])
            with open (f"images/image.jpg", "wb") as file:
                file.write(image_data)
            await bot.send_photo(message.chat.id, f'images/image.jpg', reply_to_message_id=message.id)
        else:
            await message.reply_text("Возникла ошибка, попробуйте еще раз", reply_to_message_id=message.id)
    else:
        await message.reply_text("Введите запрос")
def button_filter(button):
   async def func(_, __, msg):
       return msg.text == button.text
   return filters.create(func, "ButtonFilter", button=button)

@bot.on_message(filters.command("start"))
async def start(bot, message):
    await message.reply("Добро пожаловать!", reply_markup=buttons.kb_main)
    with open ("users.json", "r") as file:
        users = json.load(file)
    if str(message.from_user.id) not in users.keys():
        users[message.from_user.id] = 100
        with open("users.json", "w") as file:
            json.dump(users, file)

@bot.on_message(filters.command("info") | button_filter(buttons.btn_info))
async def start(bot, message):
    await message.reply("Этот бот находится в разработке")

@bot.on_message(filters.command("time"))
async def time(bot, message):
    await message.reply(current_time)

@bot.on_message(filters.command("Угадай число") | button_filter(buttons.btn_number))
async def number(bot,message):
    await message.reply("Угадай число от 1 до 5", reply_markup=ForceReply(True))
    with open("users.json","r") as file:
        users = json.load(file)
    try:
        user1 = int(message.text)  # Преобразуем введенное пользователем сообщение в число
    except ValueError:
        await message.reply("Пожалуйста, введите число от 1 до 5.")
        return
    pc = random.randint(1,5)
    print(f"Бот загадал: {pc}, Пользователь ввел: {user1}")  # Отладка
    if user1 == pc:
        await message.reply(f"Ты угадал. Бот загадал {pc}")
    else:
        await message.reply(f"Ты не угадал. Бот загадал {pc}")

@bot.on_message(filters.command("games") | button_filter(buttons.btn_games))
async def games(bot, message):
    await message.reply("Выбери игру", reply_markup=buttons.games)


@bot.on_message(filters.command("back") | button_filter(buttons.btn_back))
async def back(bot, message):
    await message.reply("Главное меню", reply_markup=buttons.kb_main)
query_text = "Введите тему изображения"
@bot.on_message(filters.command("Сгенерировать изображение") | button_filter(buttons.btn_generate))
async def generate(bot,message):
    await message.reply(query_text, reply_markup=ForceReply(True))

@bot.on_message(filters.reply)
async def reply(bot,message):
    if message.reply_to_message.text == query_text:
        query = message.text
        await message.reply_text(f"Генерирую изображение по запросу **{query}**. подождите немного")

@bot.on_message(filters.command("Камень ножницы бумага") | button_filter(buttons.btn_fgame))
async def fgame(bot, message):
    with open("users.json", "r") as file:
        users = json.load(file)
    if users[str(message.from_user.id)] >=10:
        await message.reply("Твой ход", reply_markup=buttons.kb_knb)
    else:
        await message.reply("Не хватает средств, на твоем счету {users[str(message.from_user.id}. Минимальная ставка - 10")

@bot.on_message(filters.command("Квест") | button_filter(buttons.btn_quest))
async def kvest(bot, message):
    await message.reply_text("Хотите ли вы отправиться в приключение?", reply_markup=buttons.inline_kb_start_quest)

@bot.on_callback_query()
async def handle_query(bot, query):
    if query.data == 'start_quest':
        await bot.answer_callback_query(
            query.id,
            text="Добро пожаловать в квест!",
            show_alert=True
        )
        await query.message.reply_text("Ты стоишь перед двумя дверцами, какую из них ты откроешь?",
                    reply_markup=buttons.inline_kb_choose_door)
    elif query.data == 'left_door':
        await query.message.reply_text("Ты решил открыть левую дверцу, тут лежит книга с надписью *НЕ ОТКРЫВАТЬ И НЕ ТРОГАТЬ*,"
                                       "что сделаешь?",
                    reply_markup=buttons.inline_kb_left_door)
    elif query.data == 'open_it':
        await bot.answer_callback_query(query.id,text="Ты выбрал открыть книгу, но она была с проклятием и к сожалению ты умер.",show_alert=True)
    elif query.data == 'close_it':
        await bot.answer_callback_query(query.id, text="Ты выбрал не открывать книгу, ты выжил.",show_alert=True)
    elif query.data == 'right_door':
        await query.message.reply_text("Ты выбрал правую дверцу, тут лежит странная таблетка, что сделаешь?",
                    reply_markup=buttons.inline_kb_right_door)
    elif query.data == 'eat_it':
        await bot.answer_callback_query(query.id,text="Ты выбрал сьесть таблетку, теперь у тебя есть способность читать мысли других.",show_alert=True)
    elif query.data == 'leave_it':
        await bot.answer_callback_query(query.id, text="Ты выбрал не есть таблетку и остался таким же каким и был.",show_alert=True)

@bot.on_message(button_filter(buttons.btn_rock) |
                button_filter(buttons.btn_scissors) |
                button_filter(buttons.btn_paper))
async def choice_rps(bot,message):
    with open("users.json","r") as file:
        users = json.load(file)
    rock = buttons.btn_rock.text
    scissors = buttons.btn_scissors.text
    paper = buttons.btn_paper.text
    user = message.text
    pc = random.choice([rock, scissors, paper])

    if user == pc:
        await message.reply("Ничья")
    elif (user == rock and pc == scissors) or (user == scissors and pc == paper) or (user == paper and pc == rock):
        await  message.reply(f"Ты выиграл. Бот выбрал {pc}", reply_markup=buttons.kb_knb)
        users[str(message.from_user.id)] += 10
    else:
        await message.reply(f"Ты проиграл. Бот выбрал {pc}", reply_markup=buttons.kb_knb)
        users[str(message.from_user.id)] -= 10

    with open("users.json", "w") as file:
        json.dumb(users, file)



bot.run()