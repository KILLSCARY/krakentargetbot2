import random
import sqlite3
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8091412559:AAHgqI_YrIiVrgIQ5jWhmMvtaV_2aSglNrg"

# Инициализация базы
conn = sqlite3.connect("game.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS players 
                 (user_id INTEGER PRIMARY KEY, attempts INTEGER, won INTEGER)''')
conn.commit()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    cursor.execute("INSERT OR IGNORE INTO players (user_id, attempts, won) VALUES (?, 0, 0)", (user_id,))
    conn.commit()
    await update.message.reply_text("Привет! Угадай число от 1 до 5. У тебя 3 попытки. Напиши число.")

async def handle_guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    guess_text = update.message.text

    if not guess_text.isdigit():
        await update.message.reply_text("Пожалуйста, введи число от 1 до 5.")
        return

    guess = int(guess_text)
    if guess < 1 or guess > 5:
        await update.message.reply_text("Число должно быть от 1 до 5.")
        return

    cursor.execute("SELECT attempts, won FROM players WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    if not row:
        await update.message.reply_text("Сначала напиши /start.")
        return

    attempts, won = row
    if won:
        await update.message.reply_text("Ты уже выиграл! Скидка твоя 😉")
        return

    if attempts >= 3:
        await update.message.reply_text("Ты использовал все 3 попытки 😢")
        return

    secret_number = random.randint(1, 5)
    new_attempts = attempts + 1

    if guess == secret_number:
        cursor.execute("UPDATE players SET won = 1, attempts = ? WHERE user_id = ?", (new_attempts, user_id))
        conn.commit()
        await update.message.reply_text("🎉 Поздравляю! Ты угадал. Лови ссылку на скидку: https://vk.me/grishaprotarget")
    else:
        cursor.execute("UPDATE players SET attempts = ? WHERE user_id = ?", (new_attempts, user_id))
        conn.commit()
        left = 3 - new_attempts
        await update.message.reply_text(f"Неправильно 😕 Осталось попыток: {left}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_guess))
    app.run_polling()
