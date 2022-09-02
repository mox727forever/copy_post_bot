import asyncio
import os
import random

import aiogram

bot = aiogram.Bot(os.environ.get("BOT_API_KEY"))
dp = aiogram.Dispatcher(bot)

welcome_sticks = ["CAACAgIAAx0CS-huPAABAsHIYxHYqCZhPxsMPibIuHYottixBmIAAh8hAAIReGBK-CK2oTNCkXspBA",
                  "CAACAgIAAx0CS-huPAABAsHJYxHYskb6C8w-VspE07YPDq7oMcIAAm8dAALX1mFKqyNy5IaOwfopBA",
                  "CAACAgIAAx0CS-huPAABAsHKYxHYui31pBJxecQXHytcQ1bT5-YAAiIaAAKvHGlKlEBLindYebYpBA",
                  "CAACAgIAAx0CS-huPAABAsHLYxHYwZ45lYRrTjBwVOLacnR2J00AAkIbAAI3qnFKJFqq1C7HuKIpBA",
                  "CAACAgIAAx0CS-huPAABAsHMYxHYx8B2n54RFFT3g88JUQpQPZMAAqcaAAKmBXBKRdoYIZGz9copBA"]
last_welcome_msg = []


@dp.message_handler(lambda m: m.chat.id == int(os.environ.get("WISH_CHAT_ID")), content_types=[aiogram.types.ContentTypes.NEW_CHAT_MEMBERS])
async def start_cmd(msg: aiogram.types.Message):
    global last_welcome_msg
    try:
        await msg.delete()
    except:
        pass

    for i in last_welcome_msg:
        try:
            await i.delete()
        except:
            pass

    keyboard = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(aiogram.types.KeyboardButton("Крутить по 1 💫"), aiogram.types.KeyboardButton("Крутить по 10 💫"))
    msg_1 = await msg.answer_sticker(random.choice(welcome_sticks), reply_markup=keyboard)

    keyboard = aiogram.types.InlineKeyboardMarkup()
    keyboard.add(aiogram.types.InlineKeyboardButton("Наш канал (+20 гемов в час)", url="https://t.me/+nhiU9UgPVlUyYTcy"))
    keyboard.add(aiogram.types.InlineKeyboardButton("Чат для общения", url="https://t.me/+k6t6ymljxGs3MzUy"))
    msg_2 = await msg.answer(f"""
Привет, <b>{msg.new_chat_members[0].get_mention(as_html=True)}!</b> 👋
Этот чат только для круток.
Нахождение в этом чате дает +20 гемов в час для <a href="https://t.me/genshixbot">гача бота</a>!

<b>🍀Удачных круток!</b>
    """, reply_markup=keyboard, parse_mode="HTML")

    last_welcome_msg = [msg_1, msg_2]

    await asyncio.sleep(120)

    for i in last_welcome_msg:
        try:
            await i.delete()
        except:
            pass


@dp.message_handler(lambda m: m.chat.id == int(os.environ.get("WISH_CHAT_ID")), content_types=aiogram.types.ContentType.all())
async def clear_chat(msg: aiogram.types.Message):
    try:
        await msg.delete()
    except:
        pass


@dp.message_handler(content_types=aiogram.types.ContentType.all())
async def new_post(msg: aiogram.types.Message):
    if msg.sender_chat is not None:
        if msg.sender_chat.type == "channel":
            for i in msg.entities + msg.caption_entities:
                if i.type == "custom_emoji":
                    await repost_message(msg)
                    return


async def repost_message(msg: aiogram.types.Message):
    keyboard = aiogram.types.InlineKeyboardMarkup()
    keyboard.add(aiogram.types.InlineKeyboardButton("Обновите телеграм", url="https://telegram.org/update"))
    await msg.send_copy(msg.chat.id, reply_to_message_id=msg.message_id, reply_markup=keyboard)


aiogram.executor.start_polling(dp, skip_updates=True)
