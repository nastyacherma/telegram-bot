from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from yookassa import Configuration, Payment
import uuid

# Токен Telegram-бота
TOKEN = "7774138581:AAHNYGEcigALyG0qfrJpzk-uwEiJilSgFtE"

# ЮKassa тестовый магазин
Configuration.account_id = '1090029'
Configuration.secret_key = 'test_cYlyN-1ZYj22N36Y2KymlOaP8UqXD7m5Nz3w63DP4_4'

# Ссылка на закрытый канал
CHANNEL_INVITE_LINK = "https://t.me/+abc123xyz"  # ← замени на свою


# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "привееет!\n\n"
        "create [balanced] plate — готовые рационы с посчитанным КБЖУ на каждый день: "
        "вкусные, сбалансированные и без запретов\n\n"
        "что тебя ждёт:\n"
        "• 10 готовых рационов с посчитанным КБЖУ на каждый день\n"
        "• варианты покупных/приготовленных перекусов\n"
        "• список продуктовой корзины для твоего удобства\n"
        "• возможность сохранять рецепты и возвращаться к ним в любой момент\n"
        "• доступ к новым рационам\n"
        "• чат для общения/поддержки/вопросов/рекомендаций\n\n"
        "[стоимость: 2 490₽ с доступом навсегда]")

    keyboard = [[InlineKeyboardButton("присоединяюсь!", callback_data="pay")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(text, reply_markup=reply_markup)


# Обработка нажатия на кнопку
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    print("Нажата кнопка:", query.data)

    if query.data == "pay":
        try:
            payment_id = str(uuid.uuid4())
            payment = Payment.create(
                {
                    "amount": {
                        "value": "2490.00",
                        "currency": "RUB"
                    },
                    "confirmation": {
                        "type": "redirect",
                        "return_url": "https://t.me/CreateBalancedPlate_bot"
                    },
                    "capture": True,
                    "description": "Оплата доступа к рациону"
                }, payment_id)

            await query.message.reply_text(
                f"Оплати доступ по ссылке:\n{payment.confirmation.confirmation_url}"
            )

            # Сразу выдаём ссылку (для теста)
            await query.message.reply_text(
                f"Спасибо за оплату!\nВот ссылка для входа в закрытый канал:\n{CHANNEL_INVITE_LINK}"
            )

        except Exception as e:
            print("Ошибка при создании платежа:", e)
            await query.message.reply_text(
                "Произошла ошибка при создании платежа. Попробуй ещё раз.")


# Запуск
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Бот запущен")
    app.run_polling()


if __name__ == "__main__":  # ← исправлено здесь
    main()
