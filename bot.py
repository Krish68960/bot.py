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
        [InlineKeyboardButton(" ₹100 GC = ₹1 (One Time Only)", callback_data='trial')],
        [InlineKeyboardButton(" ₹500 GC = ₹450", callback_data='basic')],
        [InlineKeyboardButton(" ₹1000 GC = ₹890", callback_data='premium')],
        [InlineKeyboardButton("₹10000 GC = ₹7999", callback_data='pro')]
        
    ]

    await update.message.reply_text(
        " *Play Store Gift Card*\n"
        "Cheapest Gift Card Provider In the Market\n\n"
        
        "🚨 *Limited Access Offer (Today Only)*\n"
        "⚠️ Offer Will Epire soon\n\n"
        
        "Choose your plan 👇\n\n"

        "Plans can be only billed once in every 7 days due to high demand\n\n"
        
        "⏳ Offer closes soon",
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
        [InlineKeyboardButton("💳 Buy Now", url=pay_link)],
        [InlineKeyboardButton("⬅️ Back", callback_data='back')]
    ]

    await query.edit_message_text(
        text=(
            f"🛡️ *Plan Selected: {plan.upper()}*\n\n"
            
            f"👥 {view_display} added GC in last 5 minutes\n"
            f"🔥 {buy_display}  members buying GC right now\n\n"
           
            f"{pressure}\n\n"
            
            "🔐 "Plans can be only billed once in every 7 days due to high demand\n\n"\n"
            
            "👇 Buy now:"
        )),
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
                "⏳ *Reminder: Offer Ending Today*\n\n"
                
                ""Plans can be only billed once in every 7 days due to high demand\n\n"\n"
                "Last Chance to grab the offer\n\n"
                
                "👉 Complete your purchase before offer closes"
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
         [InlineKeyboardButton(" ₹100 GC = ₹1 (One Time Only)", callback_data='trial')],
        [InlineKeyboardButton(" ₹500 GC = ₹450", callback_data='basic')],
        [InlineKeyboardButton(" ₹1000 GC = ₹890", callback_data='premium')],
        [InlineKeyboardButton("₹10000 GC = ₹7999", callback_data='pro')]
    ]

    await query.edit_message_text(
        text="🛡️ *Choose your plan 👇*",
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
