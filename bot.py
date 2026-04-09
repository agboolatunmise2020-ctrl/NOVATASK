import os
import asyncio
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import img2pdf

# 1. Background Flask Server for Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# 2. Telegram Bot Logic
TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Send me any photo, and I'll convert it to a PDF instantly.")

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Send a processing message
    sent_message = await update.message.reply_text("Converting to PDF... Please wait.")
    
    # Download the photo (highest quality)
    photo_file = await update.message.photo[-1].get_file()
    image_path = f"{update.message.chat_id}.jpg"
    pdf_path = f"{update.message.chat_id}.pdf"
    
    await photo_file.download_to_drive(image_path)

    # Convert Image to PDF
    try:
        with open(pdf_path, "wb") as f:
            f.write(img2pdf.convert(image_path))
        
        # Send PDF back to user
        with open(pdf_path, "rb") as f:
            await update.message.reply_document(document=f, filename="Converted_Document.pdf")
            
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")
    
    finally:
        # Cleanup files
        await sent_message.delete()
        if os.path.exists(image_path): os.remove(image_path)
        if os.path.exists(pdf_path): os.remove(pdf_path)

if __name__ == '__main__':
    # Start the web server in a separate thread
    Thread(target=run_web_server).start()

    # Start the Telegram Bot
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_image))
    
    print("Bot is starting...")
    application.run_polling()
