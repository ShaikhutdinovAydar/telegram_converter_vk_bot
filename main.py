from telegram.ext import Application, MessageHandler, filters

async def handle_document(update, context):
    await update.message.reply_text("Файл получен")

def main():
    app = Application.builder().token("TOKEN").build()
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.run_polling()

if __name__ == "__main__":
    main()
