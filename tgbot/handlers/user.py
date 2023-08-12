from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.utils.exceptions import Throttled


async def user_start(message: Message):

    await message.reply("Добро пожаловать!\n"
                        "Рад с вами познакомиться.\n"
                        "Я могу улучшить рисунок в 4 раза :-) Просто пришлите мне изображение и я вам через 1 минуту отправлю его в хорошем качестве. Я могу принимать лишь по одному арту за один раз.\n"
                        "\n"
                        "Пока что количество запросов от одного пользователя ограничено 1 за 30 секунд.")


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
