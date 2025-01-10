from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN: Final = 'YOUR_BOT_TOKEN_HERE'
BOT_USERNAME: Final = '@BOT_USERNAME_HERE'

## Replace the bot_token by the Telegram API 
## and the username of the bot