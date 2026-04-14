import os
import asyncio
import img2pdf
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# 1. Environment Variables
TOKEN = os.environ.get("BOT_TOKEN")

# Clean 3-button layout
def main_menu_keyboard():
    keyboard = [
        [KeyboardButton("🖼️ How to Convert")],
        [KeyboardButton("📄 My History"), KeyboardButton("⚖️ Privacy Policy")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "✨ *Welcome to NovaTask PDF!* ✨\n\n"
        "I convert your images into professional PDFs instantly.\n\n"
        "📸 *To start:* Simply send me a photo!"
    )
    await update.message.reply_text(welcome_text, parse_mode='Markdown', reply_markup=main_menu_keyboard())

async def handle_text_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "🖼️ How to Convert":
        await update.message.reply_text(
            "Attach a JPG or PNG and send it as a **Photo**. Please do not send it as a 'File'!",
            parse_mode='Markdown'
        )
        
    elif text == "⚖️ Privacy Policy":
        await update.message.reply_text(
            "Privacy is priority. Files are deleted immediately after conversion. We store nothing."
        )

    # NEW: Logic for the My History button
    elif text == "📄 My History":
        history_text = (
            "📋 *Your Conversion History*\n\n"
            "For your security, NovaTask operates on a **Zero-Retention** policy. "
            "We do not store your files or history on our servers.\n\n"
            "Once you download your PDF, the record is cleared! 🔒"
        )
        await update.message.reply_text(history_text, parse_mode='Markdown')
async def handle_wrong_format(update: Update, context: ContextTypes.DEFAULT_TYPE):
    correction_text = (
        "⚠️ *Wait! That's the wrong format.*\n\n"
        "You sent this as a **File/Document**. Please send it as a **Photo** (compressed)."
    )
    await update.message.reply_text(correction_text, parse_mode='Markdown')

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    processing_msg = await update.message.reply_text("📥 *Processing your PDF...*", parse_mode='Markdown')
    photo_file = await update.message.photo[-1].get_file()
    uid = update.message.chat_id
    image_path = f"img_{uid}.jpg"
    pdf_path = f"doc_{uid}.pdf"
    
    try:
        await photo_file.download_to_drive(image_path)
        with open(pdf_path, "wb") as f:
            f.write(img2pdf.convert(image_path))
        with open(pdf_path, "rb") as f:
            await update.message.reply_document(document=f, filename="NovaTask_Document.pdf")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error processing image.")
    finally:
        await processing_msg.delete()
        if os.path.exists(image_path): os.remove(image_path)
        if os.path.exists(pdf_path): os.remove(pdf_path)

# --- NEW ASYNC MAIN FOR PYTHON 3.14 ---
async def main():
    if not TOKEN:
        print("ERROR: BOT_TOKEN variable is missing!")
        return

    print("Worker starting... Connecting to Telegram.")
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_image))
    application.add_handler(MessageHandler(filters.Document.IMAGE | filters.Document.ALL, handle_wrong_format))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_buttons))
    
    # This starts the bot properly in the current event loop
    async with application:
        await application.initialize()
        await application.start()
        print("Bot is now polling...")
        await application.updater.start_polling(drop_pending_updates=True)
        # Keep the bot running until it's stopped
        while True:
            await asyncio.sleep(1)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
