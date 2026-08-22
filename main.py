import os
import logging
from google import genai
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Logging Setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Get API Keys
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "").strip()
GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "").strip()

# Initialize Gemini Client
client = genai.Client(api_key=GEMINI_KEY)

# الموديلات المتاحة للتجريب التلقائي
MODELS_TO_TRY = ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-2.0-flash"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أهلاً بك! أنا بوت الذكاء الاصطناعي الخاص بك. اسألني أي سؤال وسأجيبك فوراً! 🤖✨"
    )

async def ai_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_chat_action("typing")

    for model_name in MODELS_TO_TRY:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=user_text,
            )
            if response and response.text:
                await update.message.reply_text(response.text)
                return
        except Exception as e:
            logging.error(f"Failed with {model_name}: {e}")
            continue

    await update.message.reply_text("عذراً، تعذر الاتصال بالخدمة حالياً. حاول مجدداً بعد قليل.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_reply))

    app.run_polling()
