import os
import asyncio
from flask import Flask
from threading import Thread
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import img2pdf

# 1. Background Flask Server
app = Flask(__name__)

@app.route('/')
def home():
    return "SwiftPDF is active."

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# 2. Telegram Bot Logic
TOKEN = os.environ.get("BOT_TOKEN")

# Removed "Support" - Clean 3-button layout
def main_menu_keyboard():
    keyboard = [
        [KeyboardButton("🖼️ How to Convert")],
        [KeyboardButton("📄 My History"), KeyboardButton("⚖️ Privacy Policy")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "✨ *Welcome to SwiftPDF!* ✨\n\n"
        "I convert your images into professional PDFs instantly.\n\n"
        "📸 *To start:* Simply send me a photo!"
    )
    await update.message.reply_text(
        welcome_text, 
        parse_mode='Markdown', 
        reply_markup=main_menu_keyboard()
    )

async def handle_text_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "🖼️ How to Convert":
        await update.message.reply_text("Attach a JPG or PNG and send it as a **Photo**. Please do not send it as a 'File' or 'Document'!")
    elif text == "⚖️ Privacy Policy":
        await update.message.reply_text("Privacy is priority. Files are deleted immediately after conversion. We store nothing.")

# NEW: Correction Handler for wrong file types
async def handle_wrong_format(update: Update, context: ContextTypes.DEFAULT_TYPE):
    correction_text = (
        "⚠️ *Wait! That's the wrong format.*\n\n"
        "You sent this as a **File/Document**. To convert it, please send it as a **Photo** (compressed).\n\n"
        "💡 *How?* When attaching the image, make sure the 'Send as file' option is **unchecked**."
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
            await update.message.reply_document(
                document=f, 
                filename="SwiftPDF_Document.pdf",
                caption="✅ Converted successfully!"
            )
            
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: Please try a standard JPG or PNG photo.")
    
    finally:
        await processing_msg.delete()
        if os.path.exists(image_path): os.remove(image_path)
        if os.path.exists(pdf_path): os.remove(pdf_path)

if __name__ == '__main__':
    Thread(target=run_web_server, daemon=True).start()

    application = ApplicationBuilder().token(TOKEN).build()
    
    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_image))
    
    # This catches anything sent as a DOCUMENT/FILE instead of a PHOTO
    application.add_handler(MessageHandler(filters.Document.IMAGE | filters.Document.ALL, handle_wrong_format))
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_buttons))
    
    print("Bot is polling with Error Correction...")
    application.run_polling(drop_pending_updates=True)
