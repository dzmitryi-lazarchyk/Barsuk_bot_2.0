from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.models.database import User


async def user_start(message: Message):
    await message.answer("""Здравствуйте! Данный тедеграм-бот был создан для того, 
чтобы вы всегда были в курсе продукции бара. 
Используйте кнопку \'Menu\' для управления ботом.""")




def register_base_commands(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")