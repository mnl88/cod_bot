from aiogram import types
from misc import dp
import config
import time
import asyncio


@dp.message_handler(user_id=config.manile_id, content_types=types.ContentTypes.ANY)
async def all_other_messages(message: types.Message):
    await message.reply(str(message.date.time()))
    await asyncio.sleep(1)
    await message.reply("3", reply=False)
    await asyncio.sleep(1)
    await message.reply("2", reply=False)
    await asyncio.sleep(1)
    await message.reply("1", reply=False)
    await asyncio.sleep(1)
    await message.reply("Серёжка Фастовец - долбоёб!", reply=False)


# def tic():
#     return 'at %1.1f seconds' % (time.time() - start)
#
#
# async def gr1():
#     # Busy waits for a second, but we don't want to stick around...
#     print('gr1 started work: {}'.format(tic()))
#     await asyncio.sleep(2)
#     print('gr1 ended work: {}'.format(tic()))
#
#
# async def gr2():
#     # Busy waits for a second, but we don't want to stick around...
#     print('gr2 started work: {}'.format(tic()))
#     await asyncio.sleep(2)
#     print('gr2 Ended work: {}'.format(tic()))
#
#
# async def gr3():
#     print("Let's do some stuff while the coroutines are blocked, {}".format(tic()))
#     await asyncio.sleep(1)
#     print("Done!")
#
#
# async def main():
#     tasks = [gr1(), gr2(), gr3()]
#     await asyncio.gather(*tasks)
#
#
# asyncio.run(main())
