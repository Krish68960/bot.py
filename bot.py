import os
import random
import asyncio
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
    "🚨 Threat alerts increasing rapidly",
    "⚠️ High risk devices detected today",
    "🔥 Unusual signup activity right now",
    "⏳ Access window closing soon",
    "⚡ Demand spike detected"
]

# ================= START =================
async def start(update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔥 ₹1 Trial", callback_data='trial')],
        [InlineKeyboardButton("💼 ₹99 Monthly", callback_data='basic')],
        [InlineKeyboardButton("🚀 ₹199 Premium", callback_data='premium')],
        [InlineKeyboardButton("👑 ₹299 Pro", callback_data='pro')]
    ]

    await update.message.reply_text(
        "🛡️ *MaxMDR Security*\n"
        "Real-Time Protection for Your Device\n\n"
        
        "🚨 *Limited Access Window (Today Only)*\n"
        "⚠️ Rising Android threats detected in India\n\n"
        
        "Choose your protection plan 👇\n\n"
        
        "⏳ Access closes soon",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# ================= BUTTON =================
async def button(update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    plan = query.data
    pay_link = PAYMENT_LINKS[plan]

    # dynamic numbers
    view_count = random.randint(1800, 6200)
    buy_count = random.randint(400, 3200)

    view_display = f"{view_count/1000:.1f}K"
    buy_display = f"{buy_count/1000:.1f}K"

    pressure = random.choice(pressure_lines)

    keyboard = [
        [InlineKeyboardButton("💳 Activate Now", url=pay_link)],
        [InlineKeyboardButton("⬅️ Back", callback_data='back')]
    ]

    await query.edit_message_text(
        text=(
            f"🛡️ *Plan Selected: {plan.upper()}*\n\n"
            
            f"👥 {view_display} users securing devices now\n"
            f"🔥 {buy_display} activated protection today\n\n"
            
            f"{pressure}\n\n"
            
            "🔐 Secure your device before next threat wave\n"
            "⏳ Price & access may change anytime\n\n"
            
            "👇 Complete your activation:"
        ),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

    # ⏳ start follow-up reminder
    user_id = query.from_user.id
    context.job_queue.run_once(reminder, 120, data=user_id)

# ================= REMINDER =================
async def reminder(context: ContextTypes.DEFAULT_TYPE):
    user_id = context.job.data

    try:
        await context.bot.send_message(
            chat_id=user_id,
            text=(
                "⏳ *Reminder: Your access is still pending*\n\n"
                
                "⚠️ Threat activity is increasing rapidly\n"
                "🔥 Many users already activated protection\n\n"
                
                "👉 Complete your setup before access closes"
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
        [InlineKeyboardButton("🔥 ₹1 Trial", callback_data='trial')],
        [InlineKeyboardButton("💼 ₹99 Monthly", callback_data='basic')],
        [InlineKeyboardButton("🚀 ₹199 Premium", callback_data='premium')],
        [InlineKeyboardButton("👑 ₹299 Pro", callback_data='pro')]
    ]

    await query.edit_message_text(
        text="🛡️ *Choose your protection plan 👇*",
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
