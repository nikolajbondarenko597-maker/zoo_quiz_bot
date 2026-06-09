from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from data.quiz_data import QUESTIONS, ANIMALS
from keyboards.main import get_question_keyboard
from utils.scoring import get_initial_scores
from utils.logger import setup_logger
import logging

# Создаем роутер
router = Router()
logger = logging.getLogger(__name__)


# Класс состояний викторины
class QuizStates(StatesGroup):
    answering = State()  # Состояние: пользователь отвечает на вопрос

# Обработчик нажатия на кнопку "Начать викторину"
@router.callback_query(F.data == "start_quiz")
async def start_quiz(callback: CallbackQuery, state: FSMContext):
    """Запускает викторину с первого вопроса."""
    # Инициализируем словарь баллов в FSM-хранилище
    await state.update_data(scores=get_initial_scores(), current_question=0)
    
    # Показываем первый вопрос
    await show_question(callback, state, question_index=0)

async def show_question(callback: CallbackQuery, state: FSMContext, question_index: int):
    """Показывает вопрос с указанным индексом."""
    # Устанавливаем состояние "отвечает на вопрос"
    await state.set_state(QuizStates.answering)
    await state.update_data(current_question=question_index)
    
    question = QUESTIONS[question_index]
    question_number = question_index + 1
    total_questions = len(QUESTIONS)
    
    # Формируем текст вопроса
    text = (
        f"📝 <b>Вопрос {question_number} из {total_questions}</b>\n\n"
        f"{question['text']}"
    )
    
    # Получаем клавиатуру с вариантами ответов
    keyboard = get_question_keyboard(question_index)
    
    # Отправляем или редактируем сообщение
    try:
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    except Exception:
        # Если не удалось отредактировать (например, сообщение слишком старое), отправляем новое
        await callback.message.answer(text, reply_markup=keyboard, parse_mode="HTML")
    
    await callback.answer()

# Обработчик выбора варианта ответа
@router.callback_query(QuizStates.answering, F.data.startswith("answer_"))
async def process_answer(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает ответ пользователя и переходит к следующему вопросу."""
    # Разбираем callback_data: "answer_0_2" -> вопрос 0, вариант 2
    _, question_index_str, option_index_str = callback.data.split("_")
    question_index = int(question_index_str)
    option_index = int(option_index_str)
    
    # Получаем текущие данные из FSM
    data = await state.get_data()
    scores = data["scores"]
    
    # Получаем баллы за выбранный вариант
    question = QUESTIONS[question_index]
    option_scores = question["options"][option_index]["scores"]
    
    # Добавляем баллы к соответствующим животным
    for animal_id, points in option_scores.items():
        scores[animal_id] += points
    
    # Сохраняем обновлённые баллы
    await state.update_data(scores=scores)
    
    logger.info(f"Пользователь {callback.from_user.id} ответил на вопрос {question_index + 1}")
    
    # Проверяем, есть ли следующий вопрос
    next_question_index = question_index + 1
    
    if next_question_index < len(QUESTIONS):
        # Показываем следующий вопрос
        await show_question(callback, state, next_question_index)
    else:
        # Викторина завершена — переходим к показу результата
        # Импортируем функцию показа результата (создадим в results.py)
        from routers.results import show_result
        await show_result(callback, state, scores)

# Обработчик кнопки "Попробовать ещё раз"
@router.callback_query(F.data == "restart_quiz")
async def restart_quiz(callback: CallbackQuery, state: FSMContext):
    """Перезапускает викторину с самого начала."""
    # Очищаем предыдущее состояние
    await state.clear()
    
    # Инициализируем новые данные
    await state.update_data(scores=get_initial_scores(), current_question=0)
    
    # Показываем первый вопрос
    await show_question(callback, state, question_index=0)
    
    logger.info(f"Пользователь {callback.from_user.id} перезапустил викторину")