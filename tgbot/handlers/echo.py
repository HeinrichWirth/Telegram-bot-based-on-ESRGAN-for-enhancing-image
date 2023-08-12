from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hcode
import logging
from tgbot.middlewares.environment import rate_limit
from datetime import datetime

import os

def log_stats(user_id):
    now = datetime.now()
    timestamp = now.strftime("%d/%m/%Y_%H:%M:%S")
    with open('stats.txt', 'a') as f:
        f.write(f'{timestamp} , {user_id}\n')


@rate_limit(2)
async def bot_echo(message: types.Message):
    bot = message.bot
    text = [
        "Эхо без состояния.",
        "Сообщение:",
        message.text
    ]
    log_stats(message.from_user.id)
    await message.answer('\n'.join(text))

async def bot_echo_all(message: types.Message, state: FSMContext):
    state_name = await state.get_state()
    text = [
        f'Эхо в состоянии {hcode(state_name)}',
        'Содержание сообщения:',
        hcode(message.text)
    ]

    await message.answer('\n'.join(text))


def register_echo(dp: Dispatcher):
    dp.register_message_handler(bot_echo, content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(bot_echo_all, state="*", content_types=types.ContentTypes.TEXT)
