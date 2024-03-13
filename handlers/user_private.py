from aiogram.filters import CommandStart, Command
from aiogram import types, Router


user_private_router = Router()

@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('Это была команда старт')


@user_private_router.message(Command('menu'))
async def echo(message: types.Message):
    # await bot.send_message(message.from_user.id, 'Ответ')
    await message.answer("Вот меню:")
    # await message.reply(message.text)
    # text: str = message.text
    # if text in ['Привет', 'привет', 'hi', 'Hi', 'Hello']:
    #     await message.answer('И тебе привет!')
    # elif text in ['Пока', 'пока', 'пакеда', 'До свидания', 'Goodbye']:
    #     await message.answer('И тебе пока!')
    # else:
    #     await message.answer(message.text)

@user_private_router.message(Command('command1'))
async def echo(message: types.Message):
    # await bot.send_message(message.from_user.id, 'Ответ')
    await message.answer("Это первая команда")