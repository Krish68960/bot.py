import os
import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

PAYMENT_LINKS = {
    "trial": "https://rzp.io/l/trial",
    "basic": "https://rzp.io/l/99",
    "premium": "https://rzp.io/l/199",
    "pro": "https://rzp.io/l/299"
}

pressure_lines = [
    "🚨 High demand right now",
    "⚠️ Offer ending soon",
    "🔥 Selling fast today",
    "⏳ Limited access window",
    "⚡ Price may increase anytime"
]

# ================= START =================
async def start(update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("₹100 GC = ₹1 (One Time)", callback_data='trial')],
        [InlineKeyboardButton("₹500 GC = ₹450", callback_data='basic')],
        [InlineKeyboardButton("₹1000 GC = ₹890", callback_data='premium')],
        [InlineKeyboardButton("₹10000 GC = ₹7999", callback_data='pro')]
    ]

    await update.message.reply_text(
        "🎁 *Play Store Gift Card*\n"
        "Cheapest Gift Card Provider\n\n"
        
        "🚨 *Limited Offer (Today Only)*\n"
        "⚠️ Offer will expire soon\n\n"
        
        "Choose your plan 👇\n\n"
        
        "🔐 Plans can be billed once every 7 days\n\n"
        
        "⏳ Offer closing soon",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# ================= BUTTON =================
async def button(update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    plan = query.data
    pay_link = PAYMENT_LINKS[plan]

    view_count = random.randint(1800, 6200)
    buy_count = random.randint(400, 3200)

    view_display = f"{view_count/1000:.1f}K"
    buy_display = f"{buy_count/1000:.1f}K"

    pressure = random.choice(pressure_lines)

    keyboard = [
        [InlineKeyboardButton("💳 Buy Now", url=pay_link)],
        [InlineKeyboardButton("⬅️ Back", callback_data='back')]
    ]

    await query.edit_message_text(
        text=(
            f"🎯 *Selected Plan: {plan.upper()}*\n\n"
            f"👥 {view_display} users viewing now\n"
            f"🔥 {buy_display} bought today\n\n"
            f"{pressure}\n\n"
            "🔐 Plans can be billed once every 7 days\n\n"
            "👇 Complete your purchase:"
        ),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

    # Reminder after 2 min
    context.job_queue.run_once(reminder, 120, data=query.from_user.id)

# ================= REMINDER =================
async def reminder(context: ContextTypes.DEFAULT_TYPE):
    user_id = context.job.data

    try:
        await context.bot.send_message(
            chat_id=user_id,
            text=(
                "⏳ *Reminder: Offer Ending Soon*\n\n"
                "🔐 Limited purchase window active\n\n"
                "🔥 High demand right now\n\n"
                "👉 Complete your purchase before it closes"
            ),
            parse_mode="Markdown"
        )
    except:
        pass

# ================= BACK =================
async def back(update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("₹100 GC = ₹1 (One Time)", callback_data='trial')],
        [InlineKeyboardButton("₹500 GC = ₹450", callback_data='basic')],
        [InlineKeyboardButton("₹1000 GC = ₹890", callback_data='premium')],
        [InlineKeyboardButton("₹10000 GC = ₹7999", callback_data='pro')]
    ]

    await query.edit_message_text(
        text="🎁 *Choose your plan 👇*",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# ================= MAIN =================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button, pattern='^(trial|basic|premium|pro)$'))
app.add_handler(CallbackQueryHandler(back, pattern='^back$'))

print("Bot is running...")
app.run_polling()
