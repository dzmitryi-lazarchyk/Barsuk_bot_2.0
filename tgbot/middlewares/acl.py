from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from tgbot.models.database import User


class ACLMiddleware(BaseMiddleware):
    async def on_pre_process_update(self, update:types.Update, data:dict):
        print(update)
        if update.my_chat_member:
            id=update.my_chat_member.from_user.id
            name = update.my_chat_member.from_user.full_name
            if update.my_chat_member.new_chat_member.status == "member":
                await User.add(id=id, name=name)
            elif update.my_chat_member.new_chat_member.status=="kicked":
                await User.delete(id=id)