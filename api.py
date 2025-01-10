from typing import Final
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters, ConversationHandler
from token_1 import TOKEN, BOT_USERNAME
import logging


# add
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

GENDER, PHOTO, LOCATION, BIO = range(4)



# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'Hello! I am {BOT_USERNAME}, Thanks for chatting with me! Sana All!')
    return GENDER

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'Hello! I am {BOT_USERNAME}, how can I help you?')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command!')


async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        "I see! Please send me a photo of yourself, "
        "so I know what you look like, or send /skip if you don't want to.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return PHOTO


async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the photo and asks for a location."""
    user = update.message.from_user
    photo_file = await update.message.photo[-1].get_file()
    await photo_file.download_to_drive("user_photo.jpg")
    logger.info("Photo of %s: %s", user.first_name, "user_photo.jpg")
    await update.message.reply_text(
        "Gorgeous! Now, send me your location please, or send /skip if you don't want to."
    )

    return LOCATION


async def skip_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips the photo and asks for a location."""
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    await update.message.reply_text(
        "I bet you look great! Now, send me your location please, or send /skip."
    )

    return LOCATION


async def location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the location and asks for some info about the user."""
    user = update.message.from_user
    user_location = update.message.location
    logger.info(
        "Location of %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude
    )
    await update.message.reply_text(
        "Maybe I can visit you sometime! At last, tell me something about yourself."
    )

    return BIO


async def skip_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips the location and asks for info about the user."""
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    await update.message.reply_text(
        "You seem a bit paranoid! At last, tell me something about yourself."
    )

    return BIO


async def bio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the info about the user and ends the conversation."""
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text("Thank you! I hope we can talk again some day.")
    
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

# Responses
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Hey there! How are you?'
    if 'how are you?' in processed:
        return 'I am good! Thanks for asking!'
    if 'good' in processed:
        return 'That is great to hear!'
    if 'bye' in processed:
        return 'Goodbye! Have a great day!'
    if 'sana all' in processed:
        return 'Sana All! Ano?'
    if 'i love you' in processed:
        return 'I love you too!'
    if 'i hate you' in processed:
        return 'I am sorry to hear that!'
    if 'i am sorry' in processed:
        return 'No worries! I understand!'
    if 'thank you' in processed:
        return 'You are welcome!'
    if 'what is your name?' in processed:
        return 'My name is Christian Chanbot!'
    if 'what is your purpose' in processed:
        return 'I am here to help you!'
    if 'who created you?' in processed:
        return 'I was created by Christian Barbosa!'

    return 'I am sorry! I do not understand that!'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text
    message_type: str = update.message.chat.type

    print(f'User({update.message.from_user.id}) in {message_type}: "{text}"')

    # Handle message differently for group and private chats
    if message_type == 'group':
        if BOT_USERNAME in text:
            text = text.replace(BOT_USERNAME, '').strip()
        else:
            return

    response: str = handle_response(text)
    print('Bot:', response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(CommandHandler('gender', gender))
    app.add_handler(CommandHandler('photo', photo))
    app.add_handler(CommandHandler('skip_photo', skip_photo))
    app.add_handler(CommandHandler('location', location))
    app.add_handler(CommandHandler('skip_location', skip_location))
    app.add_handler(CommandHandler('bio', bio))
    app.add_handler(CommandHandler('cancel', cancel))
    

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.Regex("^(Boy|Girl|Other)$"), gender))
    app.add_handler(MessageHandler(filters.PHOTO, photo))
    app.add_handler(MessageHandler(filters.LOCATION, location))
    

    # Errors
    app.add_error_handler(error)

    # Polling
    print('Polling...')
    #app.run_polling(poll_interval=3)
    app.run_polling(allowed_updates=Update.ALL_TYPES)
