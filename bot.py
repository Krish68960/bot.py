import os
import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

# Get token from environment (IMPORTANT for Railway)
TOKEN = os.getenv("TOKEN")
print("TOKEN:", TOKEN)
# Your Razorpay payment links
PAYMENT_LINKS = {
    "trial": "https://rzp.io/l/trial",
    "basic": "https://rzp.io/l/99",
    "premium": "https://rzp.io/l/199",
    "pro": "https://rzp.io/l/299"
}

# Urgency / pressure lines
pressure_lines = [
    "⏳ Only few spots left",
    "🔥 High demand right now",
    "⚠️ Offer ending in few hours",
    "👥 Many users are viewing this plan",
    "🚀 Selling fast today",
    "⚡ Price may increase anytime"
]

# Start command
async def start(update, context):
    keyboard = [
        [InlineKeyboardButton("🔥 ₹1 Trial", callback_data='trial')],
        [InlineKeyboardButton("💰 ₹99 Monthly", callback_data='basic')],
        [InlineKeyboardButton("🚀 ₹199 Premium", callback_data='premium')],
        [InlineKeyboardButton("👑 ₹299 Pro", callback_data='pro')]
    ]

    await update.message.reply_text(
        "🚨 LIMITED TIME OFFER (Today Only)\n\n"
        "Protect your phone from hackers & scams ⚠️\n\n"
        "Choose your plan 👇\n\n"
        "🔥 ₹1 Trial (First 100 users)\n"
        "💰 ₹99 Monthly (Most Popular)\n"
        "🚀 ₹199 Premium (Extra Protection)\n"
        "👑 ₹299 Pro (Full Security)\n\n"
        "⏳ Offer expires soon!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Button click handler
async def button(update, context):
    query = update.callback_query
    await query.answer()

    plan = query.data
    pay_link = PAYMENT_LINKS[plan]

    pressure = random.choice(pressure_lines)
    view_count = random.randint(15, 60)
    buy_count = random.randint(5, 30)

    keyboard = [
        [InlineKeyboardButton("💳 Pay Now", url=pay_link)],
        [InlineKeyboardButton("⬅️ Back", callback_data='back')]
    ]

    await query.edit_message_text(
        text=f"⚡ You selected: {plan.upper()}\n\n"
             f"👥 {view_count} users viewing this\n"
             f"🔥 {buy_count} bought today\n"
             f"{pressure}\n\n"
             "⏳ Complete payment now 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Back button
async def back(update, context):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("🔥 ₹1 Trial", callback_data='trial')],
        [InlineKeyboardButton("💰 ₹99 Monthly", callback_data='basic')],
        [InlineKeyboardButton("🚀 ₹199 Premium", callback_data='premium')],
        [InlineKeyboardButton("👑 ₹299 Pro", callback_data='pro')]
    ]

    await query.edit_message_text(
        text="🚨 LIMITED TIME OFFER (Today Only)\n\nChoose your plan 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Run bot
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button, pattern='^(trial|basic|premium|pro)$'))
app.add_handler(CallbackQueryHandler(back, pattern='^back$'))

print("Bot is running...")
app.run_polling()
