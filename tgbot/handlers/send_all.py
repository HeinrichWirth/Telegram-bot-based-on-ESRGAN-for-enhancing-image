from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hcode
import logging
from tgbot.middlewares.environment import rate_limit
from datetime import datetime
import pandas as pd
import os






async def send_to_all(message: types.Message):

    bot = message.bot
    # Считываем файл со статистикой
    m = pd.read_csv('tgbot_template-1\file.csv')
    # Преобразуем столбец с ID в лист
    list_user = m['user_id'].unique().tolist()
    # Получаем сообщение, которое нужно отправить всем пользователям
    text = message.text.replace('/send_all ', '')
    # Отправляем сообщение всем пользователям
    for user_id in list_user:
        try:
            await bot.send_message(user_id, text)
        except:
            pass
    await message.reply('Рассылка выполнена!')



def send_all(dp: Dispatcher):
    dp.register_message_handler(send_to_all, commands=["send_all"], is_admin=True)