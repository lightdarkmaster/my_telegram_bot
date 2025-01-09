# my_telegram_bot
# Telegram Bot

This is a simple Telegram bot built using Python and the `python-telegram-bot` library. The bot can respond to commands, handle user messages, and provide interactive responses based on predefined conditions.

## Features

- **Start Command**: Greets the user with a friendly message.
- **Help Command**: Provides information on how the bot can assist.
- **Custom Command**: Demonstrates a user-defined command.
- **Text Responses**: Handles user messages and responds based on specific keywords or phrases.
- **Group Chat Support**: Detects and processes messages where the bot is mentioned.

## Prerequisites

- Python 3.8 or later
- A Telegram bot token from [BotFather](https://core.telegram.org/bots#botfather)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install dependencies:
   ```bash
   pip install python-telegram-bot
   ```

3. Set up your bot token:
   - Replace the `TOKEN` variable in the code with your bot token.

## Usage

1. Run the bot:
   ```bash
   python bot.py
   ```

2. Interact with your bot on Telegram using the following commands:
   - `/start`: Start the bot and get a welcome message.
   - `/help`: Get assistance on how to use the bot.
   - `/custom`: Execute a custom command.

3. Send text messages for keyword-based responses, such as:
   - "Hello"
   - "How are you?"
   - "Thank you"

## File Structure

```
.
├── bot.py          # Main bot script
├── .gitignore      # Ignored files
└── README.md       # Documentation
```

## Example Commands and Responses

| Command / Message  | Bot Response                            |
|--------------------|-----------------------------------------|
| `/start`           | "Hello! I am @your_bot_name!"          |
| `/help`            | "How can I help you?"                 |
| "Hello"           | "Hey there! How are you?"             |
| "Sana All"        | "Sana All! Ano?"                      |
| "Bye"             | "Goodbye! Have a great day!"          |

## Customization

- To add new commands, define a new async function and add it as a handler:
  ```python
  async def new_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
      await update.message.reply_text("This is a new command!")
  
  app.add_handler(CommandHandler('newcommand', new_command))
  ```

- To add new responses, update the `handle_response` function:
  ```python
  if 'new keyword' in processed:
      return 'This is a custom response!'
  ```

## License

This project is licensed under the MIT License. Feel free to use and modify it as needed.

