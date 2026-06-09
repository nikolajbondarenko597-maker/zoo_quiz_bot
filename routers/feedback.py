from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter

from keyboards.main import get_back_to_start_keyboard
from utils.logger import setup_logger
import logging

router = Router()
logger = logging.getLogger(__name__)


# Состояния для сбора отзыва
class FeedbackStates(StatesGroup):
    waiting_for_feedback = State()  # Ожидание текста отзыва


# Обработчик кнопки "Оставить отзыв"
@router.callback_query(F.data == "leave_feedback")
async def start_feedback(callback: CallbackQuery, state: FSMContext):
    """Запрашивает у пользователя отзыв."""
    await state.set_state(FeedbackStates.waiting_for_feedback)
    
    await callback.message.edit_text(
        "📝 <b>Оставьте отзыв</b>\n\n"
        "Нам важно ваше мнение! Напишите, что вам понравилось в викторине "
        "или что можно улучшить.\n\n"
        "Просто отправьте сообщение текстом.",
        parse_mode="HTML"
    )
    await callback.answer()


# Обработчик получения текста отзыва
@router.message(FeedbackStates.waiting_for_feedback)
async def process_feedback(message: Message, state: FSMContext):
    """Сохраняет отзыв пользователя."""
    feedback_text = message.text
    
    # Логируем отзыв (в реальном проекте можно сохранять в базу данных)
    logger.info(f"=== ОТЗЫВ ОТ ПОЛЬЗОВАТЕЛЯ {message.from_user.id} ===")
    logger.info(f"Имя: {message.from_user.full_name}")
    logger.info(f"Username: @{message.from_user.username}")
    logger.info(f"Отзыв: {feedback_text}")
    logger.info("=" * 50)
    
    # Очищаем состояние
    await state.clear()
    
    # Отправляем подтверждение
    await message.answer(
        "✅ <b>Спасибо за ваш отзыв!</b>\n\n"
        "Мы обязательно учтём ваше мнение для улучшения бота.",
        reply_markup=get_back_to_start_keyboard(),
        parse_mode="HTML"
    )