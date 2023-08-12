from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hcode
import logging
from io import BytesIO
import os
import re
from datetime import datetime, timedelta
import subprocess
from tgbot.handlers.echo import log_stats


async def save_photo(message:types.Message):
    bot = message.bot
    path_in = 'in'
    path_out = 'out'

    now = datetime.now()

    # Вычитаем 6 часа из текущего времени
    offset_hours = 6
    offset = timedelta(hours=offset_hours)
    adjusted_time = now - offset

    # Форматируем время в строку
    timestamp = adjusted_time.strftime("%d_%m_%Y_%H_%M_%S")
    photo = message.photo[-1]
    print(photo)
    user_id = message.from_user.id
    if photo['width'] <= 1280 and photo['height'] <=1280:
        await photo.download(destination_file= os.path.join(path_in ,f'{user_id}{timestamp}.jpg'))
        subprocess.call(f'python Real-ESRGAN\\inference_realesrgan.py -n RealESRGAN_x4plus_anime_6B -i tgbot_template-1\\in\\{user_id}{timestamp}.jpg -o tgbot_template-1\\out\\')
        print('готово')
        await bot.send_document(chat_id=message.chat.id, document= types.InputFile(f'tgbot_template-1\\out\\{user_id}{timestamp}_out.jpg'))
        log_stats(message.from_user.id)
    else:
        await bot.send_message(message.chat.id, "Извини. Скорее всего разврешение твоего изображения более 1280 px по одной из сторон. Что бы не перегружать сервер мне пришлось ограничить размер изображения.")

def register_save_photo(dp: Dispatcher):
    dp.register_message_handler(save_photo, content_types=types.ContentTypes.PHOTO)