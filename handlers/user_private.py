from aiogram.filters import CommandStart, Command, or_f
from aiogram import types, Router, F
from aiogram.enums import ParseMode
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_get_products
from filters.chat_types import ChatTypeFilter
from aiogram.utils.formatting import (
    as_list,
    as_marked_section,
    Bold,
)  # Italic, as_numbered_list и тд
from kbds.reply import get_keyboard

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    # await message.answer("Привет, я виртуальный помощник", reply_markup=reply.test_kbd)
    await message.answer("Привет, я виртуальный помощник",
                         # reply_markup=reply.start_kb3.as_markup(
                         reply_markup=get_keyboard(
                             "Меню",
                             "О магазине",
                             "Варианты оплаты",
                             "Варианты доставки",
                             placeholder="Что вас интересует?",
                             sizes=(2, 2)
                         ),
                         )


@user_private_router.message(or_f(Command("menu"), (F.text.lower() == "меню")))
async def menu_cmd(message: types.Message, session: AsyncSession):
    # await bot.send_message(message.from_user.id, "Ответ")
    for product in await orm_get_products(session):
        await message.answer_photo(
            product.image,
            caption=f"<strong>{product.name}\
                    </strong>\n{product.description}\nСтоимость: {round(product.price, 2)}",
        )
    await message.answer("Вот меню:")
    # await message.reply(message.text)
    # text: str = message.text
    # if text in ["Привет", "привет", "hi", "Hi", "Hello"]:
    #     await message.answer("И тебе привет!")
    # elif text in ["Пока", "пока", "пакеда", "До свидания", "Goodbye"]:
    #     await message.answer("И тебе пока!")
    # else:
    #     await message.answer(message.text)

@user_private_router.message(F.text.lower() == "о магазине")
@user_private_router.message(Command("about"))
async def about_cmd(message: types.Message):
    await message.answer("О нас:")

@user_private_router.message(F.text.lower() == "варианты оплаты")
@user_private_router.message(Command("payment"))
async def payment_cmd(message: types.Message):

    text = as_marked_section(
        Bold("Варианты оплаты:"),
    "Картой в боте",
        "При получении карта/кеш",
        "В заведении",
        marker="✅ ",
    )
    await message.answer(text.as_html())


@user_private_router.message(
    F.text.lower().contains("доставк") | (F.text.lower() == "варианты доставки"))
@user_private_router.message(Command("shipping"))
async def filter_cmd(message: types.Message):

    text = as_list(as_marked_section(
        Bold("Варианты доставки/заказа:"),
        "Курьер",
        "Самовынос (сейчас прибегу заберу)",
        "Покушаю у вас (сейчас прибегу)",
        marker="✅ "
    ),
        as_marked_section(
            Bold("Нельзя:"),
            "Почта",
            "Голуби",
            marker="❌ "
        ),
        sep="\n---------------------\n"
    )
    await message.answer(text.as_html())

# @user_private_router.message(F.contact)
# async def get_contact(message: types.Message):
#     await message.answer("Номер получен")
#     await message.answer(str(message.contact.phone_number))
#
# @user_private_router.message(F.location)
# async def get_location(message: types.Message):
#     await message.answer("Локация получена")
#     await message.answer(str(message.location))