from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import get_main_menu, get_items_keyboard, get_crypto_details

# Определение состояний
class CryptoStates(StatesGroup):
    WAITING_FOR_CATEGORY = State()
    WAITING_FOR_ITEM = State()
    WAITING_FOR_QUANTITY = State()

# Регистрация обработчиков
def register_handlers(dp: Dispatcher):
    @dp.message_handler(commands=['start'])
    async def send_welcome(message: types.Message):
        await message.reply("*👋 Добро пожаловать в Crypto Support Bot! 💸*\nЯ помогу с вопросами по криптовалютам.\n*📍 Шаг 1:* Выберите категорию:", reply_markup=get_main_menu())

    @dp.message_handler(commands=['cancel'], state='*')
    async def cancel_action(message: types.Message, state: FSMContext):
        await state.finish()
        await message.reply("*Действие отменено.*\nВыберите категорию:", reply_markup=get_main_menu())

    @dp.message_handler(state=CryptoStates.WAITING_FOR_CATEGORY)
    async def process_category(message: types.Message, state: FSMContext):
        categories = ["📈 Курсы криптовалют", "💰 Кошельки", "🔒 Безопасность", "❓ Помощь"]
        if message.text not in categories:
            await message.reply("Пожалуйста, выберите категорию из меню.")
            return
        await state.update_data(category=message.text)
        await CryptoStates.WAITING_FOR_ITEM.set()
        await message.reply(f"*📍 Шаг 2:* Выберите вопрос в категории {message.text}:", reply_markup=get_items_keyboard(message.text))

    @dp.message_handler(state=CryptoStates.WAITING_FOR_ITEM)
    async def process_item(message: types.Message, state: FSMContext):
        items = {
            "📈 Курсы криптовалют": ["BTC", "ETH", "USDT"],
            "💰 Кошельки": ["Metamask", "Trust Wallet"],
            "🔒 Безопасность": ["2FA", "Phishing"],
            "❓ Помощь": ["FAQ", "Контакты"]
        }
        user_data = await state.get_data()
        category = user_data.get('category')
        if message.text not in items.get(category, []):
            await message.reply("Пожалуйста, выберите вопрос из меню.")
            return
        await state.update_data(item=message.text)
        await CryptoStates.WAITING_FOR_QUANTITY.set()
        await message.reply(f"*📍 Шаг 3:* Укажите, сколько информации нужно (например, 1 для кратко, 2 для подробно):", reply_markup=get_crypto_details())

    @dp.message_handler(state=CryptoStates.WAITING_FOR_QUANTITY)
    async def process_quantity(message: types.Message, state: FSMContext):
        if not message.text.isdigit():
            await message.reply("Пожалуйста, введите число (например, 1 или 2).")
            return
        quantity = int(message.text)
        user_data = await state.get_data()
        category = user_data.get('category')
        item = user_data.get('item')
        await state.finish()
        await message.reply(f"*Ваш запрос:*\nКатегория: {category}\nВопрос: {item}\nУровень детализации: {quantity}\n\n*Ответ:* Скоро добавим информацию! 😎", reply_markup=get_main_menu())