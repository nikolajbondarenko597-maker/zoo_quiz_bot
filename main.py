import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from utils.logger import setup_logger

# Импортируем роутер start
from routers import start, quiz, results, feedback, contact 

async def main():
    setup_logger()
    logger = logging.getLogger(__name__)
    
    print("=" * 50)
    print("ЗАПУСК БОТА")
    print("=" * 50)
    
    if not BOT_TOKEN:
        logger.error("❌ Токен бота не найден! Проверьте файл .env")
        return
    
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Подключаем роутер start
    dp.include_router(start.router)
    dp.include_router(quiz.router)
    dp.include_router(results.router)
    dp.include_router(feedback.router)
    dp.include_router(contact.router)
    
    try:
        me = await bot.get_me()
        logger.info(f"✅ Бот подключен! Username: @{me.username}")
    except Exception as e:
        logger.error(f"❌ Ошибка подключения: {e}")
        return
    
    logger.info("🚀 Запускаем polling...")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"❌ Ошибка polling: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен пользователем.")