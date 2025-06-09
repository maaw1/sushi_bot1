from aiogram.dispatcher.filters.state import State, StatesGroup

class CryptoStates(StatesGroup):
    WAITING_FOR_CATEGORY = State()
    WAITING_FOR_ITEM = State()
    WAITING_FOR_QUANTITY = State()