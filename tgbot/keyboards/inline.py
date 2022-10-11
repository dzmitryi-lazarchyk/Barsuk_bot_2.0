from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

taps_callback = CallbackData("taps", "current_page", "to_page")


def inline_constructor(current_page:str=None, to_page:str=None):
    # keyboard=None
    if current_page == 'beer_taps_list':
        keyboard = InlineKeyboardMarkup(
            row_width=3,
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Показать по позции",
                        callback_data=taps_callback.new(current_page=current_page,
                                                        to_page='by_one',
                                                        )
                                        ),
                ]
            ]
        )
        return keyboard
    else:
        keyboard = InlineKeyboardMarkup(
            row_width=3,
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="⬅️",
                        callback_data=taps_callback.new(to_page="Previous",
                                                        current_page=current_page,
                                                        )),
                    InlineKeyboardButton(
                        text=str(current_page),
                        callback_data=taps_callback.new(to_page="all_pages",
                                                        current_page=current_page,
                                                        )
                    ),
                    InlineKeyboardButton(
                        text="➡️",
                        callback_data=taps_callback.new(to_page="Next",
                                                        current_page=current_page,
                                                        )
                    )
                ],
                [    InlineKeyboardButton(
                        text="Показать списком",
                        callback_data=taps_callback.new(to_page="beer_taps_list",
                                                        current_page=current_page,
                                                        )
                    ),
                ]
                            ]
        )
    return keyboard