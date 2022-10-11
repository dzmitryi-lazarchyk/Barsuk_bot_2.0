from aiogram.dispatcher.filters.state import StatesGroup, State


class Jars(StatesGroup):
    menu = State()
    brewery = State()
    beer = State()