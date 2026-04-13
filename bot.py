import os
import asyncio
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_LINK = "https://t.me/+AyXFqTTaNEVmNjM1"
SUPPORT_USER = "@maxpromarketer"

def main_menu_keyboard():
    keyboard = [
        [KeyboardButton("📊 Market Research Portal")],
        [KeyboardButton("🧠 Strategy Education"), KeyboardButton("🛡️ Risk Analysis")],
        [KeyboardButton("⚖️ Privacy Policy"), KeyboardButton("🆘 Support")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👋 *Welcome to NovaTask Assistant*\n\n"
        "Your hub for professional market research and strategy education. "
        "We provide the tools and data needed for disciplined market analysis.\n\n"
        "Select a resource below to begin."
    )
    await update.message.reply_text(welcome_text, parse_mode='Markdown', reply_markup=main_menu_keyboard())

async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "📊 Market Research Portal":
        await update.message.reply_text(
            "✅ *Access Authorized.*\n\nYou can now access our community research channel for real-time market insights:",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🚀 Enter Portal", url=CHANNEL_LINK)]]),
            parse_mode='Markdown'
        )
    elif text == "🧠 Strategy Education":
        await update.message.reply_text("🔍 *Educational Insights*\n\nWe focus on technical analysis, price action, and volume-weighted strategies to help users understand market movements.", parse_mode='Markdown')
    elif text == "🛡️ Risk Analysis":
        await update.message.reply_text("🛡️ *Risk Framework*\n\nProper analysis requires a strict risk-to-reward ratio. We advocate for capital preservation and disciplined execution.", parse_mode='Markdown')
    elif text == "⚖️ Privacy Policy":
        await update.message.reply_text("Privacy is priority. We do not store personal data.")
    elif text == "🆘 Support":
        await update.message.reply_text(f"For technical inquiries: {SUPPORT_USER}")

async def main():
    if not TOKEN: return
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))
    async with application:
        await application.initialize()
        await application.start()
        await application.updater.start_polling(drop_pending_updates=True)
        while True: await asyncio.sleep(1)

if __name__ == '__main__':
    try: asyncio.run(main())
    except KeyboardInterrupt: pass
