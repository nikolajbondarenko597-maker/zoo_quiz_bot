from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from keyboards.main import get_share_keyboard

from data.quiz_data import ADOPTION_TEXT
from utils.scoring import calculate_result
from utils.logger import setup_logger
import logging
import os

router = Router()
logger = logging.getLogger(__name__)


async def show_result(callback: CallbackQuery, state: FSMContext, scores: dict):
    """Показывает результат викторины — тотемное животное пользователя."""
    # Определяем победившее животное
    winner = calculate_result(scores)
    winner_id = None
    
    # Находим ID животного по имени
    from data.quiz_data import ANIMALS
    for animal_id, animal_data in ANIMALS.items():
        if animal_data["name"] == winner["name"]:
            winner_id = animal_id
            break
    
    # Формируем текст результата
    result_text = (
        f"🎉 <b>Викторина завершена!</b>\n\n"
        f"🐾 Твоё тотемное животное в Московском зоопарке — <b>{winner['name']}</b>!\n\n"
        f"{winner['description']}"
        f"{ADOPTION_TEXT}"
    )
    
    # Получаем клавиатуру с кнопками действий
    share_keyboard(callback.bot.username)
    
    # Пытаемся отправить картинку животного, если она есть
    image_path = winner.get("image")
    if image_path and os.path.exists(image_path):
        try:
            photo = FSInputFile(image_path)
            await callback.message.answer_photo(
                photo=photo,
                caption=result_text,
                reply_markup=keyboard,
                parse_mode="HTML"
            )
            # Удаляем старое сообщение с вопросом
            await callback.message.delete()
        except Exception as e:
            logger.warning(f"Не удалось отправить картинку: {e}")
            await callback.message.edit_text(result_text, reply_markup=keyboard, parse_mode="HTML")
    else:
        # Если картинки нет, просто редактируем текст
        await callback.message.edit_text(result_text, reply_markup=keyboard, parse_mode="HTML")
    
    # Сбрасываем состояние FSM
    await state.clear()
    await callback.answer("Викторина завершена! 🎉")

# Обработчик кнопки "Взять под опеку"
@router.callback_query(F.data.startswith("adopt_"))
async def show_adoption_info(callback: CallbackQuery):
    """Показывает подробную информацию о программе опеки."""
    # Извлекаем ID животного из callback_data
    animal_id = callback.data.split("_")[1]
    
    from data.quiz_data import ANIMALS
    animal = ANIMALS.get(animal_id)
    
    if not animal:
        await callback.answer("Информация о животном не найдена", show_alert=True)
        return
    
    text = (
        f"💚 <b>Программа «Возьми животное под опеку»</b>\n\n"
        f"🐾 <b>{animal['name']}</b>\n\n"
        f"Хотите поддержать этого замечательного обитателя Московского зоопарка?\n\n"
        f"Становясь опекуном, вы:\n"
        "• Вносите вклад в сохранение биоразнообразия\n"
        "• Получаете возможность навещать своего подопечного\n"
        "• Узнаёте новости о его жизни и самочувствии\n"
        "• Поддерживаете природоохранную деятельность зоопарка\n\n"
        f"👉 <a href='https://moscowzoo.ru/support/help-zoo/adopt-animal/'>Узнать подробнее и взять под опеку</a>\n\n"
        f"📞 По всем вопросам обращайтесь к нашим сотрудникам через бота."
    )
    
    from keyboards.main import get_back_to_start_keyboard
    await callback.message.edit_text(text, reply_markup=get_back_to_start_keyboard(), parse_mode="HTML")
    await callback.answer()