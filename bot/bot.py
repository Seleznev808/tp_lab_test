from telegram import Message, Update
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)

import messages as messages
from config import DEFAULT_LANGUAGE, TOKEN
from db import insert
from keyboards import (
    get_choose_language_keyboard,
    get_more_keyboard,
    get_start_keyboard
)
from logger import logger
from screenshot import get_screenshot
from utils import (
    get_screenshot_message,
    get_screenshot_path,
    get_whois,
    is_valid_url,
    get_request_info
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['language'] = DEFAULT_LANGUAGE
    keyboard = get_start_keyboard(context, messages.language_selection)
    await update.message.reply_text(
        messages.welcome_message[context.user_data['language']],
        reply_markup=keyboard
    )


async def choose_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = get_choose_language_keyboard()
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        messages.choose_language[context.user_data.get('language', DEFAULT_LANGUAGE)],
        reply_markup=keyboard
    )


async def start_with_selected_language(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    query = update.callback_query
    context.user_data['language'] = query.data
    keyboard = get_start_keyboard(context, messages.language_selection)
    await query.answer()
    await query.edit_message_text(
        messages.welcome_message[context.user_data['language']],
        reply_markup=keyboard
    )


async def send_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    language = context.user_data.get('language', DEFAULT_LANGUAGE)
    temp_message = await _send_temp_message(update, language)
    url, valid = is_valid_url(update.message.text)
    if not valid:
        return await temp_message.edit_text(messages.error_url[language])
    request_info = get_request_info(url, update)
    screenshot_path = get_screenshot_path(url, update)
    title, execution_time = await get_screenshot(url, screenshot_path)
    if not title or not execution_time:
        return await temp_message.edit_text(messages.error_url[language])
    await insert(request_info, screenshot_path, execution_time)
    await temp_message.delete()
    await update.message.reply_photo(
        screenshot_path,
        get_screenshot_message(title, url, execution_time, language),
        reply_to_message_id=update.message.id,
        parse_mode=ParseMode.HTML,
        reply_markup=get_more_keyboard(context, messages.more, request_info['website'])
    )


async def _send_temp_message(update: Update, language) -> Message:
    return await update.message.reply_text(
        messages.temp_message[language],
        reply_to_message_id=update.message.id
    )


async def show_whois(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    whois_info_message = await get_whois(
        query.data, context.user_data.get('language', DEFAULT_LANGUAGE)
    )
    await query.answer(whois_info_message, show_alert=True)


def main() -> None:
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT, send_screenshot))
    app.add_handler(CallbackQueryHandler(choose_language, pattern='^language$'))
    app.add_handler(CallbackQueryHandler(start_with_selected_language, pattern='^ru|en$'))
    app.add_handler(CallbackQueryHandler(show_whois))

    app.run_polling()


if __name__ == '__main__':
    main()
