#!/usr/bin/env python
"""
Telegram Bot with OpenAI integration.

This bot uses OpenAI API to respond to user messages intelligently.
"""
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Define a command handler. These usually take the two arguments update and context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text("Shalom! Я отвечаю через OpenAI. Задавай любые вопросы!")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = (
        "🤖 *Бот с интеграцией OpenAI*\n\n"
        "Я использую искусственный интеллект для ответов на ваши вопросы!\n\n"
        "*Доступные команды:*\n"
        "/start - Начать общение с ботом\n"
        "/help - Показать это сообщение\n\n"
        "*Как пользоваться:*\n"
        "Просто отправьте мне любое сообщение или вопрос, "
        "и я отвечу с помощью OpenAI! 🚀"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send user message to OpenAI and return response."""
    user_message = update.message.text
    
    try:
        # Send message to OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a soviet comrade helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        
        # Get AI response
        ai_response = response.choices[0].message.content
        
        # Reply to user with AI response
        await update.message.reply_text(ai_response.strip())
        
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {str(e)}")


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()