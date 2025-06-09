from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(KeyboardButton("📈 Курсы криптовалют"), KeyboardButton("💰 Кошельки"))
    markup.add(KeyboardButton("🔒 Безопасность"), KeyboardButton("❓ Помощь"))
    return markup

def get_items_keyboard(category):
    items = {
        "📈 Курсы криптовалют": ["BTC", "ETH", "USDT"],
        "💰 Кошельки": ["Metamask", "Trust Wallet"],
        "🔒 Безопасность": ["2FA", "Phishing"],
        "❓ Помощь": ["FAQ", "Контакты"]
    }
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for item in items.get(category, []):
        markup.add(KeyboardButton(item))
    return markup

def get_crypto_details():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("📊 Кратко", callback_data="details_brief"),
               InlineKeyboardButton("📚 Подробно", callback_data="details_full"))
    markup.add(InlineKeyboardButton("📞 Связаться с поддержкой", callback_data="support"))
    return markup