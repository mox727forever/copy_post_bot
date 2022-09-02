import os

import aiogram

bot = aiogram.Bot(os.environ.get("BOT_API_KEY"))
dp = aiogram.Dispatcher(bot)


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


aiogram.executor.start_polling(dp)
