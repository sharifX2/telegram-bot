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

# إعداد التسجيل
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# تهيئة مفتاح Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# تعليمات الشخصية للبوت
SYSTEM_PROMPT = "أنت بوت ذكي ومساعد محترف على تلجرام. تم تطويرك وتصميمك بالكامل بواسطة المطور Sharif."

# تجهيز النموذج
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أهلاً بك! أنا بوت الذكاء الاصطناعي الخاص بـ Sharif. اسألني أي سؤال وسأجيبك فوراً! 🤖✨"
    )

async def ai_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_chat_action("typing")

    try:
        response = model.generate_content(user_text)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ أثناء معالجة الطلب: {e}")

if __name__ == "__main__":
    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_reply))

    app.run_polling()
