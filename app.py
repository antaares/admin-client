from aiogram import executor

from loader import dp, db
import middlewares, filters, handlers



async def on_startup(dispatcher):
    try:
        db.create_table_users()
    except Exception as e:
        pass


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
