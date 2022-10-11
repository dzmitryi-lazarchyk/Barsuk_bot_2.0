from typing import Optional

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class TapsFilter(BoundFilter):
    key='taps'

    def __init__(self, taps:Optional[bool]=None):
        self.taps=taps

    async def check(self, obj) -> bool:
        return obj.data.startswith("taps")

class BreweryMsg(BoundFilter):
    key = '/brewery'

    def __init__(self, brewery:Optional[bool]=None):
        self.brewery = brewery

    def check(self, msg: types.Message) -> bool:
        return msg.text.startswith("/brewery")

class BreweryInline(BoundFilter):
    key = 'sort'

    def __init__(self, brewery:Optional[bool]=None):
        self.brewery = brewery

    async def check(self, query: types.InlineQuery) -> bool:
        return query.query.startswith("пивоварня")

class SortInline(BoundFilter):
    key = 'sort'

    def __init__(self, sort:Optional[bool]=None):
        self.sort = sort

    async def check(self, query: types.InlineQuery) -> bool:
        return query.query.startswith("сорт")