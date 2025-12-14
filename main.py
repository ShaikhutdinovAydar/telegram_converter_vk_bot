import os
from datetime import datetime
import requests
import httpx
from converter import get_result_file
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

load_dotenv()
BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document
    tg_file = await doc.get_file()

    path = doc.file_name
    await tg_file.download_to_drive(path)

    await update.message.reply_text("Файл получен")
    result = get_result_file(path)
    async with httpx.AsyncClient(timeout=30) as client:
        with open(result, "rb") as f:
            await client.post(
                N8N_WEBHOOK_URL,
                files={"file": f},
                data={
                    "file_name": doc.file_name,
                    "uploader": update.message.from_user.username,
                    "mime_type": doc.mime_type,
                    "file_size": doc.file_size,
                    "time_stamp": f"{datetime.now()}",
                }
            )

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
app.run_polling()

#{{ $('Workflow Configuration').item.binary['file'] }}