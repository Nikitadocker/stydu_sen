from orca.orca import start
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Define a command handler. These usually take the two arguments update and context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    await update.message.reply_text("Shalom!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

application = ApplicationBuilder.token("8148916624:AAFDrszZwYR955VZyD3PWswEjLdamnxjyzk").build()





application.add_handler(CommandHandler(["start"], start))

application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

application.run_polling(allowed_updates=Update.ALL_TYPES)