from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8091412559:AAHgqI_YrIiVrgIQ5jWhmMvtaV_2aSglNrg"  # вставь свой токен

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Это мини-игра с кракеном 🐙")

# Основной запуск
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.run_polling()

if __name__ == "__main__":
    main()
