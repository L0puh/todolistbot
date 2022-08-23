from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from database import sq_db


class FSMChange(StatesGroup):
    primary = State()
    date = State() 

async def change_task_start(mes:types.CallbackQuery):
    await FSMChange.primary.set()
    global text 
    text = mes.data.replace('ch ', '')
    await mes.message.answer('What the primary?')

async def change_primary(mes:types.Message, state:FSMContext):
    async with state.proxy() as data: 
        data['primary'] = mes.text 
    await FSMChange.next()
    await mes.answer('Write the date')

async def change_date(mes: types.Message, state: FSMContext):
    async with state.proxy() as data: 
        data['date'] = mes.text 
    await sq_db.change_task(text, state)
    await mes.answer('Done!') 
    await state.finish() 
