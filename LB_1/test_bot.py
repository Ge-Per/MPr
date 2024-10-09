import logging
from config import TOKEN
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

logger = logging.getLogger(__name__)


current_layout = 'en_to_ru'  # начальная раскладка: англ на ру

MENU_TEXT = "<b>Выберите направление смены раскладки:</b>\n\n"


KEYBOARD_LAYOUT = InlineKeyboardMarkup([
    [InlineKeyboardButton("Английская → Русская", callback_data='en_to_ru')],
    [InlineKeyboardButton("Русская → Английская", callback_data='ru_to_en')]
])


def change_layout(text):
    global current_layout

    if current_layout == 'en_to_ru':
        eng_to_rus = str.maketrans(
            "qwertyuiop[]asdfghjkl;'zxcvbnm,.QWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>`~",
            "йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮёЁ"
        )
        return text.translate(eng_to_rus)

    elif current_layout == 'ru_to_en':
        rus_to_eng = str.maketrans(
            "йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮёЁ",
            "qwertyuiop[]asdfghjkl;'zxcvbnm,.QWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>`~"
        )
        return text.translate(rus_to_eng)


def layout_choice(update: Update, context: CallbackContext):
    global current_layout

    data = update.callback_query.data
    current_layout = data

    update.callback_query.answer()

    update.callback_query.message.edit_text(
        "Вы выбрали направление смены раскладки:\n" + (
            "Английская → Русская" if current_layout == 'en_to_ru' else "Русская → Английская"),
        parse_mode=ParseMode.HTML
    )


def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    switched_message = change_layout(user_message)
    update.message.reply_text(switched_message)


def start(update: Update, context: CallbackContext) -> None:
    welcome_text = (
        "<b>Добро пожаловать!</b>\n\n"
        "Используйте команду /menu, чтобы выбрать направление смены раскладки (по умолчанию стоит Английская → Русская)"
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=welcome_text,
        parse_mode=ParseMode.HTML
    )


def menu(update: Update, context: CallbackContext):
    context.bot.send_message(
        update.message.from_user.id,
        MENU_TEXT,
        parse_mode=ParseMode.HTML,
        reply_markup=KEYBOARD_LAYOUT
    )


def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("menu", menu))
    dispatcher.add_handler(CallbackQueryHandler(layout_choice))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
