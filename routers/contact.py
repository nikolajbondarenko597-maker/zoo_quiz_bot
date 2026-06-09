from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.main import get_back_to_start_keyboard
from utils.logger import setup_logger
import logging

router = Router()
logger = logging.getLogger(__name__)

# ID сотрудника зоопарка (замените на реальный ID или username)
# Можно узнать свой ID через бота @userinfobot
STAFF_ID = 1004737610  


# Состояния для связи с сотрудником
class ContactStates(StatesGroup):
    waiting_for_question = State()  # Ожидание вопроса


# Обработчик кнопки "Связаться с сотрудником"
@router.callback_query(F.data == "contact_manager")
async def start_contact(callback: CallbackQuery, state: FSMContext):
    """Запрашивает у пользователя вопрос для сотрудника."""
    await state.set_state(ContactStates.waiting_for_question)
    
    await callback.message.edit_text(
        "📞 <b>Связь с сотрудником зоопарка</b>\n\n"
        "У вас есть вопрос о программе опеки или зоопарке?\n"
        "Напишите свой вопрос, и наш сотрудник свяжется с вами в ближайшее время.",
        parse_mode="HTML"
    )
    await callback.answer()


# Обработчик получения вопроса
@router.message(ContactStates.waiting_for_question)
async def process_question(message: Message, state: FSMContext, bot: Bot):
    """Пересылает вопрос сотруднику зоопарка."""
    question_text = message.text
    user = message.from_user
    
    # Формируем сообщение для сотрудника
    staff_message = (
        f"📩 <b>Новый вопрос от пользователя</b>\n\n"
        f"👤 <b>Имя:</b> {user.full_name}\n"
        f"🆔 <b>ID:</b> <code>{user.id}</code>\n"
        f"📱 <b>Username:</b> @{user.username if user.username else 'не указан'}\n\n"
        f"❓ <b>Вопрос:</b>\n{question_text}"
    )
    
    # Пытаемся отправить сообщение сотруднику
    try:
        if STAFF_ID != 123456789:  
            await bot.send_message(
                chat_id=STAFF_ID,
                text=staff_message,
                parse_mode="HTML"
            )
            logger.info(f"Вопрос от пользователя {user.id} переслан сотруднику")
        else:
            logger.warning("ID сотрудника не настроен! Вопрос не отправлен.")
    except Exception as e:
        logger.error(f"Не удалось отправить сообщение сотруднику: {e}")
    
    # Очищаем состояние
    await state.clear()
    
    # Отправляем подтверждение пользователю
    await message.answer(
        "✅ <b>Ваш вопрос отправлен!</b>\n\n"
        "Наш сотрудник свяжется с вами в ближайшее время. "
        "Спасибо за интерес к программе опеки!",
        reply_markup=get_back_to_start_keyboard(),
        parse_mode="HTML"
    )