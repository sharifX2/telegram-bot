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

# إعداد التسجيل
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# تجهيز عميل Gemini
client = genai.Client(
    api_key="AQ.Ab8RN6L0VeeM-Ild3lwjfUu7PXAZIwmPg7dk4BmVo7uosxYYfw"
)

# تعليمات الشخصية للبوت
SYSTEM_PROMPT = """[تعليمات النظام: أنت بوت ذكي ومساعد محترف على تلجرام. تم تطويرك وتصميمك بالكامل بواسطة المطور "Sharif" (sharif_2X) باستخدام Python و Gemini API. إذا سألك أي شخص عن من صممك أو طورك، أجب فوراً وبوضوح أنك من تطوير Sharif.]\n\n"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text(
      "أهلاً بك! أنا بوت الذكاء الاصطناعي الخاص بـ Sharif. اسألني أي سؤال"
      " وحأجاوك فوراً! 🤖✨"
  )


async def ai_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_text = update.message.text
  await update.message.reply_chat_action("typing")

  try:
    # دمج تعليمات الشخصية مع نص المستخدم مباشرة
    full_prompt = SYSTEM_PROMPT + user_text

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=full_prompt,
    )
    await update.message.reply_text(response.text)
  except Exception as e:
    await update.message.reply_text(f"حدث خطأ أثناء معالجة الطلب: {e}")


if __name__ == "__main__":
  TELEGRAM_TOKEN = "8890023475:AAGQtVY5pqXQc3ciduoklUR_RJ_vSvOe3mY"

  app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

  app.add_handler(CommandHandler("start", start))
  app.add_handler(
      MessageHandler(filters.TEXT & (~filters.COMMAND), ai_reply)
  )

  print("بوت الذكاء الاصطناعي شغال توا...")
  app.run_polling()