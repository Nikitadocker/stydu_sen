from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key="my_key")

# Define a command handler. These usually take the two arguments update and context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    await update.message.reply_text("Shalom! Я отвечаю через OpenAI. Задавай любые вопросы!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
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


# Create the Application and pass it your bot's token.
application = Application.builder().token("my_token").build()

application.add_handler(CommandHandler(["start"], start))

application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

application.run_polling(allowed_updates=Update.ALL_TYPES)
