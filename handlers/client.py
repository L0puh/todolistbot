from aiogram import types, Dispatcher 
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from database import sq_db
from handlers.sort_time import sort_today
from keyboards.client_kb import kb_client, kb_cancel
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .create import *
from .change import *
from datetime import datetime


text = ''


def reg_handlers_client(dp:Dispatcher): 
   
    dp.register_message_handler(start_bot, commands= ['start'])
    
    dp.register_message_handler(create_task, lambda message: 'create' in message.text, state = None)
    dp.register_message_handler(cancel, lambda message: 'cancel' in message.text, state = '*')
    dp.register_message_handler(write_text, state = FSMClient.text)
    dp.register_message_handler(write_primary, state = FSMClient.primary)
    dp.register_message_handler(write_date, state = FSMClient.date)
   
    dp.register_message_handler(show_tasks, lambda message: 'show' in message.text)   
    dp.register_callback_query_handler(delete_task,lambda mes: mes.data and mes.data.startswith('del '))
    
    dp.register_callback_query_handler(change_task_start, lambda mes: mes.data and mes.data.startswith('ch '), state = None)
    dp.register_message_handler(change_primary, state =FSMChange.primary )
    dp.register_message_handler(change_date,  state =FSMChange.date)

    dp.register_message_handler(sort_today, lambda mes: 'today' in mes.text)
 
async def start_bot(message:types.Message):
    await message.answer(f'Hi! Welcome, {message.from_user.full_name}', reply_markup= kb_client)

async def cancel(message: types.Message, state: FSMContext):
    current_proccess = await state.get_state()
    if current_proccess == None: 
        return 
    await state.finish()
    await message.answer('Okay!', reply_markup= kb_client)

async def show_tasks(message:types.Message):
    res = await sq_db.show_all_tasks()
    if res: 
        for i in res: 
            await message.answer(f'Text: {i[0]}\nPrimary: {i[1]}\nDate:{i[2]}', \
                reply_markup= InlineKeyboardMarkup().add(InlineKeyboardButton('delete', callback_data=f'del {i[0]}'), \
                    InlineKeyboardButton('change', callback_data=f'ch {i[0]}')))
    else:
        await message.answer('Tasks not found.')

async def delete_task(message: types.CallbackQuery):
    await sq_db.delete_task(message.data.replace('del ', ''))
    await message.answer(f"Delete: {message.data.replace('del ', '')}!", show_alert = True)


