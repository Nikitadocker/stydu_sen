from orca.orca import start
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler,ContextTypes

application = ApplicationBuilder.token("TOKEN").build()



application.add_handler(CommandHandler(["start"], start))