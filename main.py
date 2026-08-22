import os
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Setup Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Get API Keys from Environment
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "").strip()
GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "").strip()

# Configure Gemini
genai.configure(api_key=GEMINI_KEY)

# قائمة الموديلات المعتمدة للتنقل التلقائي في حال تعثر أحدها
MODELS_TO_TRY = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.0-pro"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أهلاً بك! أنا بوت الذكاء الاصطناعي الخاص بك. اسألني أي سؤال وسأجيبك فوراً! 🤖✨"
    )

async def ai_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_chat_action("typing")

    # تجريب الموديلات المتاحة تلقائياً بدون إظهار أخطاء للمستخدم
    for model_name in MODELS_TO_TRY:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(user_text)
            if response and response.text:
                await update.message.reply_text(response.text)
                return
        except Exception as e:
            logging.error(f"Error with {model_name}: {e}")
            continue

    await update.message.reply_text("عذراً، حدث خطأ أثناء الاتصال بالخدمة. يرجى المحاولة لاحقاً.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_reply))

    app.run_polling()
