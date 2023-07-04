from aiogram.dispatcher.filters.state import StatesGroup, State



class AdminForm(StatesGroup):
    InputID = State()
    InputFile = State()
    Confirm = State()


class ClientForm(StatesGroup):
    InputID = State()