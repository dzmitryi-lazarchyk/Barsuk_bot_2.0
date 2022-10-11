from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputMedia

from tgbot.filters.user import TapsFilter
from tgbot.keyboards.inline import inline_constructor, taps_callback
from tgbot.models.database import Tap


async def taps_list(message:types.Message, state:FSMContext):
    beer_taps = await Tap.get_all()
    msg = []
    for beer in beer_taps:
        msg.append(f'{beer.tap}. <b>{beer.name} : {beer.brewery}</b>'
                   f'{"🍯" if "mead" in beer.sort.lower() else ""}'
                   f'{"🍅" if "Other Gose" in beer.sort.lower() else ""}\n'
                   f'{beer.sort}\n'
                   f'{beer.price_list}\n'
                   f'<a href="{beer.link}">Подробнее на Your.Beer</a>')
    await message.answer("\n\n".join(msg), disable_web_page_preview=True,
                         reply_markup=inline_constructor(current_page="beer_taps_list"))

async def taps_pagenation(cal:CallbackQuery, state:FSMContext):
    await cal.answer()
    await cal.answer(cache_time=5)
    data = cal.data
    _, current_page, to_page= data.split(":")

    bot = cal.bot
    user_id = cal.from_user.id
    message = cal.message


    beer_taps = {beer.tap:beer for beer in await Tap.get_all()}
    if to_page=="by_one":
        tap = min([int(key) for key in beer_taps.keys()])
        beer:Tap = beer_taps[tap]
        await bot.send_photo(chat_id=user_id,photo=beer.image,
                             caption=f'{tap}.<b>{beer.name} : {beer.brewery}</b>'
                                     f'{"🍯" if "Mead" in beer.sort else ""}'
                                     f'{"🍅" if "Other Gose" in beer.sort else ""}\n'
                                     f'{beer.sort}\n'
                                     f'{beer.price_list}\n'
                                     f'<a href="{beer.link}">Подробнее на Your.Beer</a>',
                             parse_mode='HTML',
                             reply_markup=inline_constructor(current_page=str(tap))
                             )
        return
    elif to_page=="Next":
        current_tap = int(current_page)
        taps = [int(key) for key in beer_taps.keys()]
        if current_tap in taps:
            current_tap_inx= taps.index(current_tap)
            try:
                tap = taps[current_tap_inx+1]
            except IndexError:
                tap=taps[0]
        else:
            tap=min([int(key) for key in beer_taps.keys()])
    elif to_page=="Previous":
        current_tap = int(current_page)
        taps = [int(key) for key in beer_taps.keys()]
        if current_tap in taps:
            current_tap_inx= taps.index(current_tap)
            try:
                tap = taps[current_tap_inx-1]
            except IndexError:
                tap=taps[-1]
        else:
            tap=min([int(key) for key in beer_taps.keys()])
    elif to_page=="all_pages":
        current_tap = int(current_page)
        taps = [int(key) for key in beer_taps.keys()]
        slices = []
        for i in range(0, len(taps), 5):
            slices.append(taps[i:i+5])
        keyboard = InlineKeyboardMarkup(row_width=4)
        for slice in slices:
            row = []
            for tap in slice:
                button = InlineKeyboardButton(
                    text=str(tap),
                    callback_data=taps_callback.new(current_page=current_page,
                                                    to_page=tap,
                                                    ))
                row.append(button)
            keyboard.row(*row)
        await message.edit_reply_markup(reply_markup=keyboard)
        return
    elif to_page == "beer_taps_list":
        await taps_list(message, state)
    else:
        tap = int(to_page)
    beer = await Tap.get(tap=tap)
    media = InputMedia(type = 'photo', media=beer.image)
    await message.edit_media(media=media,
                         reply_markup=inline_constructor(current_page=str(tap))
                         )
    await message.edit_caption(caption=f'{tap}.<b>{beer.name} : {beer.brewery}</b>'
                                       f'{"🍯" if "Mead" in beer.sort else ""}'
                                       f'{"🍅" if "Other Gose" in beer.sort else ""}\n'
                         f'{beer.sort}\n'
                         f'{beer.price_list}\n'
                         f'<a href="{beer.link}">Подробнее на Your.Beer</a>',
                         parse_mode='HTML',
                         reply_markup=inline_constructor(current_page=str(tap)
                              ))

def register_taps(dp:Dispatcher):
    dp.register_message_handler(taps_list, Command("taps"), state="*")
    dp.register_callback_query_handler(taps_pagenation, TapsFilter(), state="*")