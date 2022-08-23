from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

show_tasks = KeyboardButton('show tasks')
create_tasks = KeyboardButton('create tasks')
cancel_create = KeyboardButton ('cancel')
today_task = KeyboardButton('today')


kb_client = ReplyKeyboardMarkup(resize_keyboard= True)
kb_cancel =  ReplyKeyboardMarkup(resize_keyboard= True, one_time_keyboard= True)
kb_client.row(show_tasks, create_tasks, today_task)
kb_cancel.add(cancel_create)