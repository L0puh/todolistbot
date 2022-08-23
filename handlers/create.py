from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher 
from database import sq_db
from keyboards.client_kb import kb_client, kb_cancel
from datetime import datetime

class FSMClient(StatesGroup): 
    text = State()
    primary = State() 
    date = State() 

async def create_task(message:types.Message):
    await FSMClient.text.set()
    await message.answer('Write the text', reply_markup= kb_cancel)
    

async def write_text(message:types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text 
    await FSMClient.next() 
    await message.answer('Write the primary')

async def write_primary(message: types.Message, state: FSMContext):
    try:
        if int(message.text) > 3:
            await message.answer('Primary can be only 0,1,2,3!')
        else:
            async with state.proxy() as data: 
                data['primary'] = message.text 
            await FSMClient.next() 
            await message.answer('Which date?[YYYY:MM:DD]')
    except ValueError: 
        await message.answer('Primary can be only 0,1,2,3!')

async def write_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['date'] = message.text
    
    await sq_db.create_task_db(state)

    await message.answer('Done')
    await state.finish() 