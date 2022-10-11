from sre_constants import INFO

from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.handler import ctx_data
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputTextMessageContent

from tgbot.filters.user import BreweryInline, SortInline
from tgbot.misc.states import Jars
from tgbot.models.database import Jar


async def jars(message:types.Message):

    jars = await Jar.get_all()
    breweries = await Jar.get_column("brewery")
    sorts =  await Jar.get_column("sort")
    msg = await message.answer(text="Сортировать банки по:👇",
                               reply_markup=InlineKeyboardMarkup(
                                   inline_keyboard=[
                                       [
                                           InlineKeyboardButton(
                                               text=f"Пивоварни({len(breweries)})",
                                               switch_inline_query_current_chat="Пивоварни",
                                           ),
                                       ],
                                       [
                                           InlineKeyboardButton(
                                               text=f"Сорта({len(sorts)})",
                                               switch_inline_query_current_chat="Сорта"
                                           ),
                                       ],
                                       [
                                           InlineKeyboardButton(
                                               text=f"Все банки({len(jars)})",
                                               switch_inline_query_current_chat="Все банки"
                                           ),
                                       ]
                                   ],
                               row_width=1,
                               ))


# ****************************Sorting by brewery***********************************
async def breweries(query:types.InlineQuery, state:FSMContext):
    breweries = await Jar.get_column("brewery")
    await query.answer(
        results=[
            types.InlineQueryResultArticle(
                id=f"{brewery}",
                title=f"{brewery}",
                input_message_content=InputTextMessageContent(
                    message_text=f"Нажмите на кнопку👇"
                ),
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[[
                        InlineKeyboardButton(
                            text=f"Показать банки {brewery}",
                            switch_inline_query_current_chat=f"пивоварня {brewery}"
                        )
                    ]]
                )
            ) for brewery in sorted(breweries)
        ],
        cache_time=1
    )

async def brewery_inline(query: types.InlineQuery, state:FSMContext):
    brewery = query.query.strip('пивоварня ')
    beers = await Jar.get_several(brewery=brewery)
    await query.answer(
        results=[
            types.InlineQueryResultArticle(
                id=str(id),
                title=f"{beer}",
                description=f"{beer.sort}",
                thumb_url=f"{beer.image}",
                url=f'{beer.link}',
                input_message_content=InputTextMessageContent(
                                    message_text=f'<b>{beer.name} : {beer.brewery}</b>'\
                                 f'{"🍯" if "mead" in beer.sort.lower() else ""}'\
                                 f'{"🍅" if "Other Gose" in beer.sort.lower() else ""}\n'\
                                 f'{beer.sort}\n'\
                                 f'{beer.price_list}\n\n'\
                                 f'{beer.link}\n'\
                )) for id, beer in enumerate(sorted(beers, key=lambda x: x.name))
        ],
        cache_time=1
    )

# ****************************Sorting by sort***********************************

async def sorts(query:types.InlineQuery, state:FSMContext):
    sorts = await Jar.get_column("sort")
    sorts = set([sort.split(',')[0] for sort in sorts])
    await query.answer(
        results=[
            types.InlineQueryResultArticle(
                id=f"{sort}",
                title=f"{sort}",
                input_message_content=InputTextMessageContent(
                    message_text=f"Нажмите на кнопку👇"
                ),
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[[
                        InlineKeyboardButton(
                            text=f"Показать банки {sort}",
                            switch_inline_query_current_chat=f"сорт {sort}"
                        )
                    ]]
                )
            ) for sort in sorted(sorts)
        ],
        cache_time=1
    )

async def sort_inline(query: types.InlineQuery, state:FSMContext):
    sort = query.query.strip('сорт ')
    beers = await Jar.get_by_sort(sort=sort)
    await query.answer(
        results=[
            types.InlineQueryResultArticle(
                id=str(id),
                title=f"{beer}",
                description=f"{beer.sort}",
                thumb_url=f"{beer.image}",
                url=f'{beer.link}',
                input_message_content=InputTextMessageContent(
                                    message_text=f'<b>{beer.name} : {beer.brewery}</b>'\
                                 f'{"🍯" if "mead" in beer.sort.lower() else ""}'\
                                 f'{"🍅" if "Other Gose" in beer.sort.lower() else ""}\n'\
                                 f'{beer.sort}\n'\
                                 f'{beer.price_list}\n\n'\
                                 f'{beer.link}\n'\
                )) for id, beer in enumerate(sorted(beers, key=lambda x: x.name))
        ],
        cache_time=1
    )

async def all_jars(query:types.InlineQuery):
    beers = await Jar.get_all()
    await query.answer(
                results=[
                    types.InlineQueryResultArticle(
                        id=str(id),
                        title=f"{beer}",
                        description=f"{beer.sort}",
                        thumb_url=f"{beer.image}",
                        url=f'{beer.link}',
                        input_message_content=InputTextMessageContent(
                            message_text=f'<b>{beer.name} : {beer.brewery}</b>' \
                                         f'{"🍯" if "mead" in beer.sort.lower() else ""}' \
                                         f'{"🍅" if "Other Gose" in beer.sort.lower() else ""}\n' \
                                         f'{beer.sort}\n' \
                                         f'{beer.price_list}\n\n' \
                                         f'{beer.link}\n'
                            )) for id, beer in enumerate(sorted(beers, key=lambda x: x.name))
                        ]
    )

def register_jars(dp:Dispatcher):
    dp.register_message_handler(jars, Command("jars"), state="*")

    dp.register_inline_handler(breweries, text="Пивоварни")
    dp.register_inline_handler(brewery_inline, BreweryInline())

    dp.register_inline_handler(sorts, text="Сорта")
    dp.register_inline_handler(sort_inline, SortInline())

    # dp.register_inline_handler(all_jars, text="Все банки")
