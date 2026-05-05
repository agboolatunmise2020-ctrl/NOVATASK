import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Setup logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# 1. Define the Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton("📊 View Market Strategy", callback_data="info_page")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Welcome to NovaTask.\n\nClick below to see our current trading focus and intraday analysis.",
        reply_markup=reply_markup
    )

# 2. Define the Button Logic (The Flow)
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "info_page":
        # Second Screen: Strategy Details
        keyboard = [[InlineKeyboardButton("⚖️ Risk & Disclaimer", callback_data="disclaimer_page")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="**XAUUSD Intraday Analysis**\n\nWe focus on:\n• Market Structure\n• Liquidity\n• Execution",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    elif query.data == "disclaimer_page":
        # Third Screen: Disclaimer and Redirect
        keyboard = [
            [InlineKeyboardButton("🚀 Join Apex Entries", url="https://t.me/apexentries")],
            [InlineKeyboardButton("⬅️ Back", callback_data="info_page")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="**Information**\n\nSharing trade ideas for educational purposes only. No guaranteed results.\n\nJoin the channel to see live entries:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

# 3. Main Function to Run the Bot
def main():
    # It will look for a Variable named 'BOT_TOKEN' in your Render settings
    token = os.environ.get("BOT_TOKEN")
    
    if not token:
        print("ERROR: No BOT_TOKEN found in Environment Variables.")
        return

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_buttons))

    application.run_polling()

if __name__ == "__main__":
    main()
