from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from token_1 import TOKEN, BOT_USERNAME


# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'Hello! I am {BOT_USERNAME}, Thanks for chatting with me! Sana All!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'Hello! I am {BOT_USERNAME}, how can I help you?')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command!')

# Responses
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Hey there! How are you?'
    if 'how are you' in processed:
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
    if 'what is your name' in processed:
        return 'My name is Christian Chanbot!'
    if 'what is your purpose' in processed:
        return 'I am here to help you!'
    if 'who Created you?' in processed:
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

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polling
    print('Polling...')
    app.run_polling(poll_interval=3)
