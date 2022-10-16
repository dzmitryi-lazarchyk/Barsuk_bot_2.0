import asyncio
import aioschedule
from aiogram import Bot, Dispatcher

from tgbot.models.database import User, Tap, Jar
from utils.parse_youbeer.beer import parse_yourbear


async def new_taps(dp:Dispatcher):
    parse_beer = {beer.tap:beer for beer in parse_yourbear("taps")}
    db_beer = {beer.tap:beer for beer in await Tap.get_all()}
    result_taps=set(parse_beer.keys()) ^ set(db_beer.keys())
    if result_taps:
        users = await User.get_all()

        for tap in result_taps:
            beer = parse_beer.get(tap, db_beer.get(tap))
            if tap in parse_beer:
                msg = f'<b>🎉Новинка на кране🎉:\n</b>'\
                      f'{beer.tap}.<b>{beer.name} : {beer.brewery}</b>'\
                      f'{"🍯" if "mead" in beer.sort.lower() else ""}'\
                      f'{"🍅" if "Other Gose" in beer.sort.lower() else ""}\n'\
                      f'{beer.sort}\n'\
                      f'{beer.price_list}\n'\
                      f'<a href="{beer.link}">Подробнее на Your.Beer</a>'
                await Tap.add(parse_beer[tap])
                for user in users:
                    await dp.bot.send_photo(chat_id=user.id, photo=beer.image, caption=msg)
            else:
                msg = f'<b>Закончилось:\n</b>'\
                      f'<s>{beer.tap}.<b>{beer.name} : {beer.brewery}</b></s>'\
                      f'{"🍯" if "mead" in beer.sort.lower() else ""}'\
                      f'{"🍅" if "Other Gose" in beer.sort.lower() else ""}\n'\
                      f'{beer.sort}\n'
                await Tap.delete(tap=tap)
                for user in users:
                    await dp.bot.send_message(chat_id=user.id, text=msg)

async def new_jars(dp:Dispatcher):
    parse_beer = {beer.name:beer for beer in parse_yourbear("jars")}
    db_beer = {beer.name:beer for beer in await Jar.get_all()}
    result_jars=set(parse_beer.keys()) ^ set(db_beer.keys())
    if result_jars:
        users = await User.get_all()

        for jar in result_jars:
            beer = parse_beer.get(jar, db_beer.get(jar))
            if jar in parse_beer:
                msg = f'<b>🎉Новинка!🎉:\n</b>'\
                      f'<b>{beer.name} : {beer.brewery}</b>'\
                      f'{"🍯" if "mead" in beer.sort.lower() else ""}'\
                      f'{"🍅" if "Other Gose" in beer.sort.lower() else ""}\n'\
                      f'{beer.sort}\n'\
                      f'{beer.price_list}\n'\
                      f'<a href="{beer.link}">Подробнее на Your.Beer</a>'
                await Jar.add(parse_beer[jar])
                for user in users:
                    await dp.bot.send_photo(chat_id=user.id, photo=beer.image, caption=msg)
            else:
                msg = f'<b>Закончилось:\n</b>'\
                      f'<s><b>{beer.name} : {beer.brewery}</b></s>'\
                      f'{"🍯" if "mead" in beer.sort.lower() else ""}'\
                      f'{"🍅" if "Other Gose" in beer.sort.lower() else ""}\n'\
                      f'{beer.sort}\n'
                await Jar.delete(name=jar)
                for user in users:
                    await dp.bot.send_message(chat_id=user.id, text=msg)


async def scheduler(dp:Dispatcher):
    await new_taps(dp)
    await new_jars(dp)
    aioschedule.every(10).minutes.do(new_taps, dp)
    aioschedule.every(10).minutes.do(new_jars, dp)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)



