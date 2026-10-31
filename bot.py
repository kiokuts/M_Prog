import logging
from html import entities
from multiprocessing import context

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from telegram._utils import markup
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters, CommandHandler, CallbackQueryHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
screaming = False

FIRST_MENU = "<b>Menu 1</b>\n\n Tap to proceed."
SECOND_MENU = "<b>Menu 2</b>\n\n Tap the approriate button."

NEXT_BUTTON = "<Next>"
BACK_BUTTON = "<Back>"
TUTORIAL_BUTTON = "<Tutorial>"

FIRST_MENU_MARKUP = InlineKeyboardMarkup([[
    InlineKeyboardButton(NEXT_BUTTON, callback_data=NEXT_BUTTON),
]])
SECOND_MENU_MARKUP = InlineKeyboardMarkup([[
    InlineKeyboardButton(BACK_BUTTON, callback_data=BACK_BUTTON)],
    [InlineKeyboardButton (TUTORIAL_BUTTON, url="https://core.telegram.org/bots/api")],
    [InlineKeyboardButton ("<Video>", url="https://youtu.be/yKAHQ0jXcps?si=1w_nvbrAHR_0Cl3A")]
])

async def post_init(app) -> None:
    await app.bot.set_my_commands([
        BotCommand('start', "Hi"),
        BotCommand('menu', "Open menu"),
        BotCommand('scream', "Screaming mode"),
        BotCommand('whisper', "Whisper mode"),
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hi! I`m Kio. I can scream and whisper. Tap /menu")

async def button_tap(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data = query.data
    text = ''
    markup = None

    if data == NEXT_BUTTON:
        text = SECOND_MENU
        markup = SECOND_MENU_MARKUP
    elif data == BACK_BUTTON:
        text = FIRST_MENU
        markup = FIRST_MENU_MARKUP

    await query.answer()

    await query.message.edit_text(text, parse_mode=ParseMode.HTML, reply_markup=markup)

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(update.message.chat_id,FIRST_MENU, parse_mode=ParseMode.HTML,reply_markup=FIRST_MENU_MARKUP)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f'{update.message.from_user.first_name} wrote {update.message.text}')

    if context.user_data.get("screaming") and update.message.text:
       await context.bot.send_message (update.message.chat_id, update.message.text.upper(), entities = update.message.entities)
    else:
       await context.bot.copy_message (chat_id = update.message.chat_id, from_chat_id=update.message.chat_id, message_id=update.message.message_id)

async def scream(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["screaming"] = True
    await update.message.reply_text("Screaming mode enabled!")

async def whisper(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data ["screaming"] = False
    await update.message.reply_text("Whisper mode enabled!")

    await context.bot.copy_message(chat_id=update.message_chat.id, from_chat_id=update.message.chat_id, message_id=update.message.message_id)

def main() -> None:
    app = ApplicationBuilder().token("token_bot").post_init(post_init).build()
    app.add_handler(MessageHandler(~filters.COMMAND, echo))
    app.add_handler(CommandHandler("scream", scream))
    app.add_handler(CommandHandler("whisper", whisper))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CallbackQueryHandler(button_tap))
    app.add_handler(CommandHandler("start", start))


    app.run_polling()


if __name__ == '__main__':
    main()