from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_GROUP_ID = int(os.getenv("ADMIN_GROUP_ID"))

message_user_map = {}

async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.message
    sent = await context.bot.forward_message(chat_id=ADMIN_GROUP_ID, from_chat_id=message.chat_id, message_id=message.message_id)
    message_user_map[sent.message_id] = user.id

async def handle_admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message.reply_to_message:
        return
    original_msg_id = message.reply_to_message.message_id
    user_id = message_user_map.get(original_msg_id)
    if user_id:
        try:
            await context.bot.send_message(chat_id=user_id, text=message.text)
        except Exception as e:
            await context.bot.send_message(chat_id=ADMIN_GROUP_ID, text=f"Gagal kirim pesan ke user: {e}")
    else:
        await context.bot.send_message(chat_id=ADMIN_GROUP_ID, text="User tidak ditemukan dari pesan reply.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.PRIVATE & filters.TEXT, handle_user_message))
app.add_handler(MessageHandler(filters.ChatType.GROUPS & filters.REPLY & filters.TEXT, handle_admin_reply))
print("Bot Admin ZonaDracinId aktif...")
app.run_polling()
