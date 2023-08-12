from typing import Union
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types, Dispatcher
from aiogram.utils.exceptions import Throttled
from aiogram.dispatcher.handler import CancelHandler, current_handler
import asyncio
import emoji


tt = emoji.emojize(":smiling_face_with_open_hands:")
#class EnvironmentMiddleware(BaseMiddleware):
  #  skip_patterns = ["error", "update"]
    
  #  def __init__(self, **kwargs):
  #      super().__init__()
 #       self.kwargs = kwargs
    
 #   async def pre_process(self, obj, data, *args):
 #       data.update(**self.kwargs)
def rate_limit(limit: int, key=None):
    """
    Decorator for configuring rate limit and key in different functions.
    :param limit:
    :param key:
    :return:
    """

    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)
        return func

    return decorator


class EnvironmentMiddleware(BaseMiddleware):
    """
    Simple middleware
    """

    def __init__(self, limit=30, key_prefix='antiflood_', admins=None):
        self.rate_limit = limit
        self.prefix = key_prefix
        self.admins = set(admins) if admins else set()
        super(EnvironmentMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        """
        This handler is called when dispatcher receives a message
        :param message:
        """
        # Get current handler
        handler = current_handler.get()

        # Get dispatcher from context
        dispatcher = Dispatcher.get_current()
        # If handler was configured, get rate limit and key from handler
        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"

        # Check if the sender is an admin
        if message.from_user.id in self.admins:
            return

        # Use Dispatcher.throttle method.
        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            # Execute action
            await self.message_throttled(message, t)

            # Cancel current handler
            raise CancelHandler()

    async def message_throttled(self, message: types.Message, throttled: Throttled):
        """
        Notify user only on first exceed and notify about unlocking only on last exceed
        :param message:
        :param throttled:
        """
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            key = f"{self.prefix}_message"

        # Calculate how many time is left till the block ends
        delta = throttled.rate - throttled.delta

        # Prevent flooding
        if throttled.exceeded_count <= 2:
            await message.reply('Слишком много запросов. 1 запрос в 30 секунд. Спасибо за понимание.')

        # Sleep.
        await asyncio.sleep(delta)

        # Check lock status
        thr = await dispatcher.check_key(key)

        # If current message is not last with current key - do not send message
        if thr.exceeded_count == throttled.exceeded_count:
            await message.reply(f'Спасибо за ожидание. Вы можете отправить ещё один запрос {tt}.')