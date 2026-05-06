import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Setup logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# 1. First Screen: Welcome & Free Channel Join
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("🔘 JOIN FREE CHANNEL", url="https://t.me/apexentries")],
        [InlineKeyboardButton("✅ I Joined The Free Channel", callback_data="joined_free")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = (
        "Welcome to Apex Entries 📊\n\n"
        "Join our free public group first, watch our performance, analysis, and execution style — "
        "then apply for VIP access if you want to take your trading to the next level.\n\n"
        "Inside the free channel you’ll see:\n"
        "• Free market analysis\n• Live trade ideas\n• Gold (XAUUSD) updates\n"
        "• Educational content\n• Real execution examples\n\n"
        "━━━━━━━━━━━━━━\n"
        "After joining the free channel, return here and press the button below."
    )
    
    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup)
    else:
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup)

# 2. Button Handler for the Flow
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "joined_free":
        # Second Screen: VIP Decision
        keyboard = [
            [InlineKeyboardButton("🏆 Apply For VIP Access", callback_data="apply_vip")],
            [InlineKeyboardButton("📩 Send Message To Support", callback_data="support_info")],
            [InlineKeyboardButton("⬅️ Back", callback_data="back_to_start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = (
            "Good decision ✅\n\n"
            "Now you can apply for access to the private VIP group where we share:\n\n"
            "📊 Advanced market analysis\n🎯 Structured trade executions\n"
            "📍 Liquidity & institutional zones\n🎥 Analysis before entries\n"
            "🧠 Professional trading concepts\n\n"
            "Choose an option below 👇"
        )
        await query.edit_message_text(text, reply_markup=reply_markup)

    elif query.data == "apply_vip":
        # Third Screen: Registration Steps
        keyboard = [
            [InlineKeyboardButton("🔗 Register on UEXO", url="https://client.uexo.com/en/register?cmp=1a5u8o8w&refid=1401")],
            [InlineKeyboardButton("✅ Send ID to Support", url="https://t.me/reedexecution")],
            [InlineKeyboardButton("⬅️ Back", callback_data="joined_free")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = (
            "🔘 **Apply For VIP Access**\n\n"
            "1️⃣ Register using the official UEXO link below\n"
            "2️⃣ Verify your account\n"
            "3️⃣ Fund the account\n"
            "4️⃣ Send your account ID screenshot\n\n"
            "Once approved, you’ll receive the VIP group access link 🔐\n\n"
            "🎁 **UEXO Promotion:**\n"
            "• Get 150% bonus on your first deposit\n"
            "• Get 25% bonus on every future deposit"
        )
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

    elif query.data == "support_info":
        # Support Screen
        keyboard = [
            [InlineKeyboardButton("👉 Contact Support", url="https://t.me/reedexecution")],
            [InlineKeyboardButton("⬅️ Back", callback_data="joined_free")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = (
            "🔘 **Send Message To Support**\n\n"
            "For direct support, VIP approval, or questions regarding access:\n\n"
            "Our team is ready to assist you with your transition to VIP."
        )
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

    elif query.data == "back_to_start":
        await start(update, context)

# 3. Main Function
def main():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        print("ERROR: No BOT_TOKEN environment variable found.")
        return

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_buttons))

    application.run_polling()

if __name__ == "__main__":
    main()
