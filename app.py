import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from dotenv import find_dotenv, load_dotenv

from middlewares.db import DataBaseSession

load_dotenv(find_dotenv())

from database.engine import create_db, drop_db, session_maker

from handlers.user_private import user_private_router
from handlers.user_group import user_group_router
from handlers.admin_private import admin_router

from common.bot_cmds_list import private

# ALLOWED_UPDATES = ['message, edited_message', 'callback_query']

bot = Bot(token=os.getenv('TOKEN'), parse_mode=ParseMode.HTML)
bot.my_admins_list = []
dp = Dispatcher()

# dp.update.outer_middleware(CounterMiddleware())

dp.include_router(user_private_router)
dp.include_router(user_group_router)
dp.include_router(admin_router)

run_param = False
async def on_startup(bot):
    if run_param:
        await drop_db()
    await create_db()

async def on_shutdown(bot):
    print('Бот лег')


async def main():
    await create_db()
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    '''Чтобы бот не отвечал на сообщения если он офлайн'''
    await bot.delete_webhook(drop_pending_updates=True)
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


asyncio.run(main())
