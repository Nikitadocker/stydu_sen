#!/usr/bin/env python
"""
Telegram Bot with OpenAI integration.

This bot uses OpenAI API to respond to user messages intelligently.
"""
import logging
import os
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

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
        "/help - Показать это сообщение\n"
        "/image <описание> - Сгенерировать изображение\n\n"
        "*Как пользоваться:*\n"
        "Просто отправьте мне любое сообщение или вопрос, "
        "и я отвечу с помощью OpenAI! 🚀\n\n"
        "*Пример генерации изображения:*\n"
        "`/image красивый закат над океаном`"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generate an image using DALL-E based on user prompt."""
    # Get the prompt from the command arguments
    if not context.args:
        await update.message.reply_text(
            "❌ Пожалуйста, укажите описание изображения.\n"
            "Пример: `/image красивый закат над океаном`",
            parse_mode="Markdown"
        )
        return
    
    prompt = " ".join(context.args)
    
    # Send "generating" message
    status_message = await update.message.reply_text("🎨 Генерирую изображение, подождите...")
    
    try:
        logger.info(f"Generating image with prompt: {prompt}")
        
        # Generate image using DALL-E
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        # Get image URL
        image_url = response.data[0].url
        
        # Download image
        image_response = requests.get(image_url)
        image_response.raise_for_status()
        
        # Send image to user
        await update.message.reply_photo(
            photo=image_response.content,
            caption=f"🎨 Изображение по запросу: _{prompt}_",
            parse_mode="Markdown"
        )
        
        # Delete status message
        await status_message.delete()
        
        logger.info("Image generated and sent successfully")
        
    except Exception as e:
        logger.error(f"Error generating image: {str(e)}")
        await status_message.edit_text(f"❌ Ошибка при генерации изображения: {str(e)}")


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
        
        logger.info("Message processed successfully")
        
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        await update.message.reply_text(f"Ошибка: {str(e)}")


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("image", generate_image))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()