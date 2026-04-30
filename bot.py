import os
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- CONFIGURATION ---
# Replace with your actual token or set it in Render Environment Variables
TOKEN = os.getenv("TELEGRAM_TOKEN", "8433155630:AAHP47TfhjGYnkw5cFgqAiXgZvksNnuHs-s")
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
    # Main Buttons (Reply Keyboard)
    keyboard = [
        ["❤️ចុចទីនេះដើម្បីបើកអាខោនភ្លាមៗ❤️"],
        ["❤️ចុចទីនេះដើម្បីចូលរួមក្នុងឆានែល❤️"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    # Send the welcome image and description
    # Ensure you have a photo URL or file ID. Using a placeholder for now.
    await update.message.reply_text(text=WELCOME_TEXT)
    await update.message.reply_text(text=START_REPLY, reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Redirect all button clicks to your contact link
    text = update.message.text
    if "ចុចទីនេះ" in text:
        await update.message.reply_text(f"សូមចុចទីនេះដើម្បីបន្ត: {CONTACT_LINK}")

# --- MAIN ---
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    
    print("Bot is running...")
    app.run_polling()
