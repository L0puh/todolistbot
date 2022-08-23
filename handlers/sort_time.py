
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types
from database import sq_db
from datetime import datetime, date


async def sort_today(message:types.Message):
    today = str(date.today())
    tasks = await sq_db.show_all_tasks()
    for i in tasks:
        if today == i[2]:
            await message.answer(f'Text: {i[0]}\nPrimary: {i[1]}\nDate:{i[2]}', \
                            reply_markup= InlineKeyboardMarkup().add(InlineKeyboardButton('delete', callback_data=f'del {i[0]}'), \
                                InlineKeyboardButton('change', callback_data=f'ch {i[0]}')))
    