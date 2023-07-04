from aiogram import types

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Text
from filters.is_admin import IsAdmin

from states.form import AdminForm

from loader import dp, db



from keyboards.default.add_client import confirm_markup, add_client_markup


@dp.message_handler(IsAdmin(), Text(equals="Mijoz qo‘shish"))
async def start_add_client(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
    await message.answer("Yaxshi, menga mijoz uchun id raqam yuboring!")
    await AdminForm.InputID.set()



@dp.message_handler(state=AdminForm.InputID)
async def get_client_id(message: types.Message, state: FSMContext):
    client_id = message.text
    if db.check_id(client_id):
        await message.answer(
            text="Bu ID raqam avval ro'yxatdan o'tgan!"
        )
        await state.finish()
        await AdminForm.InputID.set()
        return
    await state.update_data(client_id=client_id)
    await message.answer(
        text="Qabul qildim, Menga mijoz uchun kerakli faylni yuboring.\n*Faqat bitta fayl qabul qilinadi!"
    )
    await AdminForm.InputFile.set()



@dp.message_handler(content_types=types.ContentTypes.DOCUMENT, state=AdminForm.InputFile)
async def get_client_file(message: types.Message, state: FSMContext):
    file_id = message.document.file_id
    await state.update_data(file_id=file_id)
    await message.answer(
        text="Qabul qildim, Mijozni qo‘shishni tasdiqlaysizmi?",
        reply_markup=confirm_markup
    )
    await AdminForm.Confirm.set()



@dp.message_handler(Text(equals="Tasdiqlayman"), state=AdminForm.Confirm)
async def confirm_add_client(message: types.Message, state: FSMContext):
    await message.answer("Yaxshi, Mijoz qo‘shildi!", reply_markup=add_client_markup)
    data = await state.get_data()
    client_id = data.get("client_id")
    file_id = data.get("file_id")
    await state.finish()
    try:
        db.add_client(client_id=client_id, file_id=file_id)
    except Exception as err:
        print(err)
        await message.answer(f"Xato yuz berdi!\nBu ID band qilingan bo‘lishi mumkin.", reply_markup=add_client_markup)


@dp.message_handler(Text(equals="Bekor qilish"), state=AdminForm.Confirm)
async def cancel_add_client(message: types.Message, state: FSMContext):
    await message.answer("Yaxshi, Mijoz qo‘shilmadi!", reply_markup=add_client_markup)
    await state.finish()