import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from config import BOT_TOKEN
from bot.handlers import (
    start_command, help_command, status_command, reset_command,
    register_name, handle_choice, cancel, REGISTER_NAME
)


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    """Основная функция запуска бота"""

    application = Application.builder().token(BOT_TOKEN).build()


    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            REGISTER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, register_name)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("reset", reset_command))


    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_choice))


    logger.info("🤖 Бот QuestChronicle запущен...")
    print("Бот успешно запущен! Для остановки нажмите Ctrl+C")

    try:
        application.run_polling()
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")


if __name__ == "__main__":
    main()