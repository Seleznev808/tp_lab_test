from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import DEFAULT_LANGUAGE


def get_start_keyboard(
    context: ContextTypes.DEFAULT_TYPE, language_selection: dict[str, str]
) -> InlineKeyboardMarkup:
    button = [
        [
            InlineKeyboardButton(
                language_selection[context.user_data['language']],
                callback_data='language'
            )
        ]
    ]
    return InlineKeyboardMarkup(button)


def get_choose_language_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton('🇺🇸 English', callback_data='en'),
            InlineKeyboardButton('🇷🇺 Русский', callback_data='ru')
        ]
    ]
    return InlineKeyboardMarkup(buttons)


def get_more_keyboard(
    context: ContextTypes.DEFAULT_TYPE, more: dict[str, str], website: str
) -> InlineKeyboardMarkup:
    button = [
        [
            InlineKeyboardButton(
                more[context.user_data.get('language', DEFAULT_LANGUAGE)],
                callback_data=website
            )
        ]
    ]
    return InlineKeyboardMarkup(button)
