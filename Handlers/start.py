from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from re import compile
from misc import dp
from config import ADMIN_ID, CHAT_TEST_ID
from .handler_2_cod_edit import add_user_to_bd_step_1


# Запускаем бот из группы
@dp.message_handler(chat_id=CHAT_TEST_ID, chat_type=['group', 'supergroup'], commands=['about_cod_bot', 'start'])
async def start_bot_not_in_the_main_group(message: types.Message):
    """Информация о боте"""
    bot_user = await dp.bot.get_me()
    main_group = message.chat.id
    bot_link = f'https://t.me/{bot_user.username}?start={main_group}'
    group_link = f'https://t.me/ruszone'
    text = [
        'Данный бот написан для предоставления пользователям информации по своей статистике в игре '
        'CALL OF DUTY MW 2019 и упрощения коммуникации участников тематической группы',
        group_link,
        '',
        'Для работы БОТА необходимо сообщить данные своей учётной записи в игре: ' + bot_link,
        '',
        'автор: @MaNiLe88'
    ]
    joined_text = '\n'.join(text)
    await message.reply(text=joined_text)


@dp.message_handler(CommandStart(compile(r"")), chat_type='private')
async def start_deep_link4(message: types.Message):
    """Информация о боте"""
    group_link = f'https://t.me/ruszone'
    deep_link_args = message.get_args()
    text = [
        'Данный бот написан для предоставления пользователям информации по своей статистике в игре '
        'CALL OF DUTY MW 2019 и упрощения коммуникации участников тематической группы',
        group_link,
        '',
        'Справка по основным командам: /help',
        '',
        'автор: @MaNiLe88'
    ]
    joined_text = '\n'.join(text)
    await message.reply(text=joined_text)
    # await message.reply(text=f'Дип_линк = {deep_link_args}')
    await add_user_to_bd_step_1(message)


# Запускаем бот из лички без диплинка
@dp.message_handler(chat_type='private', commands=['about_cod_bot', 'start'])
async def about_bot1(message: types.Message):
    """Информация о боте"""
    link = f'https://t.me/ruszone'
    text = [
        'Данный бот написан для предоставления пользователям информации по своей статистике в игре '
        'CALL OF DUTY MW 2019 и упрощения коммуникации участников тематической группы', link,
        '',
        'Для полноценной работы необходимо внести данные своей учётной записи с помощью команды: /add_me',
        '',
        'Справка по основным командам: /help',
        '',
        'автор: @MaNiLe88'
    ]
    joined_text = '\n'.join(text)
    await message.reply(text=joined_text)
