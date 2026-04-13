import os
import asyncio
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# 1. Configuration
TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_LINK = "https://t.me/+AyXFqTTaNEVmNjM1"
SUPPORT_USER = "@maxpromarketer"

# 2. Keyboards
def main_menu_keyboard():
    keyboard = [
        [KeyboardButton("📊 Access VIP Market Portal")],
        [KeyboardButton("💡 Strategy Guides"), KeyboardButton("🛡️ Risk Education")],
        [KeyboardButton("⚖️ Privacy Policy"), KeyboardButton("🆘 Support")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def channel_inline_button():
    keyboard = [[InlineKeyboardButton("🚀 Join Private Community", url=CHANNEL_LINK)]]
    return InlineKeyboardMarkup(keyboard)

# 3. Logic Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Professional, non-aggressive welcome message
    welcome_text = (
        "👋 *Welcome to NovaTask!*\n\n"
        "We provide professional tools and insights for navigating today's markets. "
        "Our goal is to assist you with disciplined strategies and community-driven data.\n\n"
        "Explore our resources below to get started."
    )
    await update.message.reply_text(
        welcome_text, 
        parse_mode='Markdown', 
        reply_markup=main_menu_keyboard()
    )

async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "📊 Access VIP Market Portal":
        await update.message.reply_text(
            "✅ *Verification Complete.*\n\nYou are invited to join our private binary insights channel. "
            "Click below to enter:",
            reply_markup=channel_inline_button(),
            parse_mode='Markdown'
        )

    elif text == "💡 Strategy Guides":
        msg = (
            "🔍 *Market Analysis Overview*\n\n"
            "We utilize a blend of technical indicators and price action. Our VIP portal covers:\n"
            "• Momentum-based execution\n"
            "• Volume profile analysis\n"
            "• Optimal entry/exit timing"
        )
        await update.message.reply_text(msg, parse_mode='Markdown')

    elif text == "🛡️ Risk Education":
        msg = (
            "🛡️ *Capital Preservation*\n\n"
            "Success in any market requires strict discipline:\n"
            "1. Define your risk before every trade.\n"
            "2. Maintain a balanced portfolio.\n"
            "3. Use data, not emotions, to drive decisions."
        )
        await update.message.reply_text(msg, parse_mode='Markdown')

    elif text == "⚖️ Privacy Policy":
        await update.message.reply_text(
            "NovaTask values your privacy. We do not store personal trading data or user history."
        )

    elif text == "🆘 Support":
        await update.message.reply_text(
            f"Questions regarding VIP access or portal tools?\n\n"
            f"Contact Support: {SUPPORT_USER}"
        )

# --- ASYNC MAIN FOR PYTHON 3.14 ---
async def main():
    if not TOKEN:
        print("ERROR: BOT_TOKEN variable is missing!")
        return

    print("NovaTask Portal starting...")
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))
    
    async with application:
        await application.initialize()
        await application.start()
        print("Bot is now polling...")
        await application.updater.start_polling(drop_pending_updates=True)
        while True:
            await asyncio.sleep(1)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
