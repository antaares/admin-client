from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Text

from loader import dp, db

from states.form import ClientForm

from keyboards.default.add_client import add_client_markup

from filters.is_admin import IsAdmin


@dp.message_handler(IsAdmin(), CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
    
    await message.answer(
        text="Assalomu alaykum, siz adminsiz!",
        reply_markup=add_client_markup
    )


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
    await message.answer(
        text="Assalomu alaykum, menga ID raqamni yuboring!"
    )
    await ClientForm.InputID.set()



@dp.message_handler(state=ClientForm.InputID)
async def get_client_id(message: types.Message, state: FSMContext):
    client_id = message.text
    if db.check_id(client_id):
        await message.answer(
            text="Bu ID raqam avval ro'yxatdan o'tgan!"
        )
        await state.finish()
        await ClientForm.InputID.set()
        return
    file_id = db.select_file_id(client_id)
    await message.answer_document(
        document=file_id,
        caption=f"{client_id} - Mijoz fayli!"
    )
    # await dp.bot.send_document(
    #     chat_id=message.from_user.id,
    #     document=(file_id, fil
    # )
    await ClientForm.InputID.set()
    await message.answer(
        text="Yaxshi, menga boshqa ID raqam yuborishingiz mumkin."
    )