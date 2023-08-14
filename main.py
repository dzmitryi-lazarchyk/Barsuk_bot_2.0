import os
import subprocess

import uvicorn

from fastapi import FastAPI, Request, Response

#!!!!!!!!!!!!!!!!!!!!!!!

import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter

from tgbot.handlers.base_commands import register_base_commands
from tgbot.handlers.jars import register_jars
from tgbot.handlers.taps import register_taps

from tgbot.middlewares import *
from tgbot.models.database import Database
from utils.parse_youbeer.task import scheduler


# API and app handling
app = FastAPI(
    title="Barsuk_bot",
)


@app.on_event("startup")
def startup_event() -> None:
    try:
        loop = asyncio.get_event_loop()
        background_tasks = set()
        task = loop.create_task(bot())
        background_tasks.add(task)
        task.add_done_callback(background_tasks.discard)
    except Exception as e:
        logging.critical(f"Error occurred while starting up app: {e}")


@app.get("/")
def root() -> str:
    return f"Bot is online"



@app.post("/terminal/run")
async def run_command(command: dict) -> str:
    try:
        output_bytes = subprocess.check_output(
            command["command"], shell=True, stderr=subprocess.STDOUT
        )
        output_str = output_bytes.decode("utf-8")
        # Split output into lines and remove any leading/trailing whitespace
        output_lines = [line.strip() for line in output_str.split("\n")]
        # Join lines with a <br> tag for display in HTML
        formatted_output = "<br>".join(output_lines)
    except subprocess.CalledProcessError as e:
        formatted_output = e.output.decode("utf-8")
    return formatted_output



logger = logging.getLogger(__name__)


def register_all_middlewares(dp, config):
    dp.setup_middleware(EnvironmentMiddleware(config=config))
    dp.setup_middleware(ACLMiddleware())


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_base_commands(dp)
    register_taps(dp)
    register_jars(dp)



async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    db = Database()




    bot['config'] = config

    register_all_middlewares(dp, config)
    register_all_filters(dp)
    register_all_handlers(dp)

    await dp.bot.set_my_commands([
        types.bot_command.BotCommand('start', 'Запустить бота'),
        types.bot_command.BotCommand('taps', 'На кранах'),
        types.bot_command.BotCommand('jars', 'Банки'),
        types.bot_command.BotCommand('settings', 'Настроики'),
        types.bot_command.BotCommand('help', 'Справка'),
    ])

    # start
    try:
        await db.create_tables()
        asyncio.create_task(scheduler(dp))
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


# Minnion run
if __name__ == "__main__":
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = os.getenv("PORT", 8080)
    uvicorn.run(app, host=HOST, port=PORT)