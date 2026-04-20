import os
import sys
from pathlib import Path

# Ensure the project root is on sys.path so Django apps are importable
sys.path.insert(0, str(Path(__file__).resolve().parent))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo.settings')

import django
django.setup()

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from asgiref.sync import sync_to_async
from decouple import config
from users.models import User


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Welcome! To receive task reminders, please send me your TaskFlow account email.'
    )


async def handle_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    email = update.message.text.strip()
    chat_id = update.effective_chat.id

    try:
        user = await sync_to_async(User.objects.get)(email__iexact=email)
        user.telegram_chat_id = chat_id
        await sync_to_async(user.save)()
        await update.message.reply_text('You are connected! You will receive task reminders here.')
    except User.DoesNotExist:
        await update.message.reply_text(
            'No account found with that email. '
            'Make sure you use the same email you registered with on TaskFlow.'
        )


if __name__ == '__main__':
    app = ApplicationBuilder().token(config('BOT_TOKEN')).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_email))
    print('Bot is running...')
    app.run_polling()
