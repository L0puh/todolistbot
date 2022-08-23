from aiogram import types, executor 
from create_bot import bot, dp 
from handlers import client
from database import sq_db
 
async def on_startup(_):
    print('[+] Bot is online')
    sq_db.create_db()
    
client.reg_handlers_client(dp)

executor.start_polling(dp, on_startup=on_startup, skip_updates= True)