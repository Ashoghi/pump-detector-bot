from telegram import Update
from telegram.ext import CommandHandler
from pump_detector import detect_pump
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! 🤖\n"
        "بات تشخیص پامپ فعال شد."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "دستورات:\n"
        "/start - شروع بات\n"
        "/help - راهنما"
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
async def pump(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) == 0:
        await update.message.reply_text(
            "استفاده:\n/pump BTCUSDT"
        )
        return

    symbol = context.args[0].upper()

    try:
        result = await detect_pump(symbol)

        if result["is_pump"]:
            text = (
                f"🚀 پامپ شناسایی شد!\n\n"
                f"نماد: {result['symbol']}\n"
                f"رشد: {result['price_change']:.2f}%\n"
                f"حجم: {result['volume']:.0f}"
            )
        else:
            text = (
                f"❌ پامپ مشاهده نشد.\n\n"
                f"نماد: {result['symbol']}\n"
                f"رشد: {result['price_change']:.2f}%\n"
                f"حجم: {result['volume']:.0f}"
            )

        await update.message.reply_text(text)

    except Exception as e:
        await update.message.reply_text(f"خطا:\n{e}")
    app.add_handler(CommandHandler("pump", pump))
