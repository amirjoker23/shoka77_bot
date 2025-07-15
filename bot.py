import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes,
)

# محیط و پیکربندی
PORT = int(os.environ.get("PORT", 8443))
BOT_TOKEN = os.environ["BOT_TOKEN"]
ADMIN_ID = int(os.environ["ADMIN_ID"])
WEBHOOK_URL = os.environ["WEBHOOK_URL"]  # مثلا: https://shoka77-bot.onrender.com/your_bot_token

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# مراحل گفتگو
(
    NAME,
    PHONE,
    NATIONAL_ID,
    MARITAL,
    ADDRESS,
    BIRTHDAY,
    JOB,
    PLAN,
    POSTAL,
    BENEFICIARY_ID,
    BENEFICIARY_BIRTHDAY,
) = range(11)

# شروع گفتگو با دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! 👋\n"
        "برای ثبت اطلاعات خود لطفاً نام و نام خانوادگی خود را وارد کنید:"
    )
    return NAME

# شروع گفتگو با دریافت پیام متنی "start" یا "استارت"
async def start_on_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! 👋\n"
        "برای ثبت اطلاعات خود لطفاً نام و نام خانوادگی خود را وارد کنید:"
    )
    return NAME

# گرفتن نام
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("📞 شماره تماس شما را وارد کنید:")
    return PHONE

# گرفتن شماره تلفن
async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['phone'] = update.message.text
    await update.message.reply_text("🆔 کد ملی خود را وارد کنید:")
    return NATIONAL_ID

# گرفتن کد ملی
async def get_national_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['national_id'] = update.message.text
    await update.message.reply_text(
        "💍 وضعیت تاهل خود را انتخاب کنید:",
        reply_markup=ReplyKeyboardMarkup(
            [["متاهل"], ["مجرد"]], one_time_keyboard=True, resize_keyboard=True
        ),
    )
    return MARITAL

# گرفتن وضعیت تاهل
async def get_marital(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['marital'] = update.message.text
    await update.message.reply_text("🏠 آدرس محل سکونت خود را وارد کنید:")
    return ADDRESS

# گرفتن آدرس
async def get_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['address'] = update.message.text
    await update.message.reply_text("🎂 تاریخ تولد خود را به فرمت YYYY/MM/DD وارد کنید:")
    return BIRTHDAY

# گرفتن تاریخ تولد
async def get_birthday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['birthday'] = update.message.text
    await update.message.reply_text("💼 شغل خود را وارد کنید:")
    return JOB

# گرفتن شغل
async def get_job(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['job'] = update.message.text
    await update.message.reply_text(
        "📅 نحوه پرداخت مورد نظر را انتخاب کنید:",
        reply_markup=ReplyKeyboardMarkup(
            [["ماهانه"], ["سالانه"], ["یکجا"]], one_time_keyboard=True, resize_keyboard=True
        ),
    )
    return PLAN

# گرفتن طرح پرداخت
async def get_plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['plan'] = update.message.text
    await update.message.reply_text("📮 کد پستی محل سکونت خود را وارد کنید:")
    return POSTAL

# گرفتن کد پستی
async def get_postal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['postal'] = update.message.text
    await update.message.reply_text("👥 کد ملی ذینفع را وارد کنید:")
    return BENEFICIARY_ID

# گرفتن کد ملی ذینفع
async def get_beneficiary_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['beneficiary_id'] = update.message.text
    await update.message.reply_text("🎁 تاریخ تولد ذینفع را به فرمت YYYY/MM/DD وارد کنید:")
    return BENEFICIARY_BIRTHDAY

# گرفتن تاریخ تولد ذینفع و پایان گفتگو
async def get_beneficiary_birthday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['beneficiary_birthday'] = update.message.text
    info = context.user_data
    msg = (
        f"📥 فرم جدید ثبت شد:\n\n"
        f"👤 نام: {info['name']}\n"
        f"📞 شماره تماس: {info['phone']}\n"
        f"🆔 کد ملی: {info['national_id']}\n"
        f"💍 وضعیت تاهل: {info['marital']}\n"
        f"🏠 آدرس: {info['address']}\n"
        f"🎂 تاریخ تولد: {info['birthday']}\n"
        f"💼 شغل: {info['job']}\n"
        f"📅 طرح پرداخت: {info['plan']}\n"
        f"📮 کد پستی: {info['postal']}\n"
        f"👥 کد ملی ذینفع: {info['beneficiary_id']}\n"
        f"🎁 تاریخ تولد ذینفع: {info['beneficiary_birthday']}"
    )
    # ارسال اطلاعات به ادمین
    await context.bot.send_message(chat_id=ADMIN_ID, text=msg)
    # پیام پایانی به کاربر
    await update.message.reply_text(
        "✅ اطلاعات شما با موفقیت ثبت شد.\n"
        "🔗 لینک پرداخت به‌زودی برای شما ارسال خواهد شد."
    )
    return ConversationHandler.END

# لغو مکالمه
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ فرآیند لغو شد.")
    return ConversationHandler.END


def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            MessageHandler(
                filters.TEXT & filters.Regex(r"(?i)^(start|استارت)$"), start_on_text
            ),
        ],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            NATIONAL_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_national_id)],
            MARITAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_marital)],
            ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_address)],
            BIRTHDAY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_birthday)],
            JOB: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_job)],
            PLAN: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_plan)],
            POSTAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_postal)],
            BENEFICIARY_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_beneficiary_id)],
            BENEFICIARY_BIRTHDAY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_beneficiary_birthday)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    logging.info(f"🌐 راه‌اندازی وبهوک روی پورت {PORT} با آدرس {WEBHOOK_URL}")

    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()
