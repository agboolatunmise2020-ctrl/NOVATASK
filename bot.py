import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Replace with your actual Bot Token from BotFather
TOKEN = "8433155630:AAHP47TfhjGYnkw5cFgqAiXgZvksNnuHs-s"

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends the first message with the first button."""
    keyboard = [[InlineKeyboardButton("📊 Explore Market Insights", callback_id="step_1")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Welcome to NovaTask AI.\n\nWe are currently focusing on high-level market data and intraday strategy. Would you like to see our current focus?",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the multi-step button progression."""
    query = update.callback_query
    await query.answer()

    if query.data == "step_1":
        # Step 2: Information about the strategy
        keyboard = [[InlineKeyboardButton("🔎 View Strategy Details", callback_data="step_2")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="Our focus is primarily on **XAUUSD Intraday Analysis**.\n\nWe utilize:\n• Market Structure\n• Liquidity Mapping\n• Precision Execution",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    elif query.data == "step_2":
        # Step 3: The Disclaimer and Final Redirect Button
        keyboard = [
            [InlineKeyboardButton("📈 Join Apex Entries", url="https://t.me/apexentries")],
            [InlineKeyboardButton("⬅️ Back", callback_data="step_1")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="**Apex Entries**\n\nSharing trade ideas for educational purposes only. No guaranteed results.\n\nReady to see the live charts?",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

def main():
    """Start the bot."""
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()
