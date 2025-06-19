from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_GROUP_ID = int(os.getenv("ADMIN_GROUP_ID"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot sudah aktif!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message:
        sender = message.from_user
        user_text = message.text or "[non-text message]"

        forward_msg = f"👤 Pesan dari @{sender.username or sender.first_name} (ID: {sender.id}):\n{user_text}"
        await context.bot.send_message(chat_id=ADMIN_GROUP_ID, text=forward_msg)
        await message.reply_text("Pesanmu sudah dikirim ke Admin. Terima kasih!")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
