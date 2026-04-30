import os
import asyncio
import nest_asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Apply fix for the "no current event loop" error
nest_asyncio.apply()

# --- CONFIGURATION ---
TOKEN = os.getenv("TELEGRAM_TOKEN", "YOUR_BOT_TOKEN_HERE")
CONTACT_LINK = "https://t.me/S_8888_ES"

# --- KHMER TEXT STRINGS ---
WELCOME_TEXT = (
    "ស្វាគមន៍មកកាន់វេបសាយ SB24 🙏\n\n"
    "🎁 ប្រូម៉ូសិនអស់ស្ទះជាមួយ SB24\n\n"
    "👉 ប្រាក់រង្វាន់ថ្ងៃ 30%\n"
    "👉 ប្រាក់រង្វាន់សប្តាហ៍ 50%\n"
    "👉 ប្រាក់រង្វាន់ខែ 100%\n\n"
    "🎁 សំណាងអាចជារបស់លោកអ្នក លីងសម្រាប់បង្កើតអាខោន:\n"
    f"{CONTACT_LINK}"
)

START_REPLY = "សូមស្វាគមន៍មកកាន់ SB24 អនឡាញកាស៊ីណូ ធំបំផុត និងគួរឱ្យទុកចិត្តបំផុត នៅក្នុងប្រទេសកម្ពុជា!!"

# --- HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["❤️ចុចទីនេះដើម្បីបើកអាខោនភ្លាមៗ❤️"],
        ["❤️ចុចទីនេះដើម្បីចូលរួមក្នុងឆានែល❤️"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(text=WELCOME_TEXT)
    await update.message.reply_text(text=START_REPLY, reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "ចុចទីនេះ" in text:
        await update.message.reply_text(f"សូមចុចទីនេះដើម្បីបន្ត: {CONTACT_LINK}")

# --- MAIN EXECUTION ---
async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot is running...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    
    # Keep the bot running
    while True:
        await asyncio.sleep(1)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except RuntimeError:
        # Fallback for environments where a loop is already running
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
