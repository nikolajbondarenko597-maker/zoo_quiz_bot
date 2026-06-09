from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data.quiz_data import QUESTIONS


def get_start_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для старта викторины."""
    builder = InlineKeyboardBuilder()
    builder.button(text="🎯 Начать викторину", callback_data="start_quiz")
    builder.button(text="ℹ️ О программе опеки", callback_data="about_adoption")
    builder.adjust(1)  # Каждая кнопка с новой строки
    return builder.as_markup()


def get_question_keyboard(question_index: int) -> InlineKeyboardMarkup:
    """Клавиатура с вариантами ответов для конкретного вопроса."""
    builder = InlineKeyboardBuilder()
    question = QUESTIONS[question_index]
    
    for i, option in enumerate(question["options"]):
        # callback_data содержит индекс вопроса и индекс варианта
        builder.button(
            text=option["text"],
            callback_data=f"answer_{question_index}_{i}"
        )
    
    builder.adjust(1)  # Каждый вариант с новой строки
    return builder.as_markup()


def get_result_keyboard(animal_id: str) -> InlineKeyboardMarkup:
    """Клавиатура после показа результата."""
    builder = InlineKeyboardBuilder()
    builder.button(text="🔄 Попробовать ещё раз", callback_data="restart_quiz")
    builder.button(text="💚 Взять под опеку", callback_data=f"adopt_{animal_id}")
    builder.button(text="📞 Связаться с сотрудником", callback_data="contact_manager")
    builder.button(text="📝 Оставить отзыв", callback_data="leave_feedback")
    builder.adjust(1)
    return builder.as_markup()


def get_back_to_start_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для возврата к началу."""
    builder = InlineKeyboardBuilder()
    builder.button(text="🏠 В главное меню", callback_data="back_to_start")
    return builder.as_markup()

def get_share_keyboard(bot_username: str) -> InlineKeyboardMarkup:
    """Клавиатура для шаринга результата в соцсетях."""
    builder = InlineKeyboardBuilder()
    
    # Ссылка на бота для шаринга
    bot_url = f"https://t.me/{bot_username}"
    
    builder.button(
        text="📤 Поделиться результатом",
        url=f"https://t.me/share/url?url={bot_url}&text=Моё%20тотемное%20животное%20в%20Московском%20зоопарке!%20Узнай%20своё%20👉"
    )
    builder.button(text="🔄 Попробовать ещё раз", callback_data="restart_quiz")
    builder.button(text="💚 Взять под опеку", callback_data="adopt")
    builder.button(text="📞 Связаться с сотрудником", callback_data="contact_manager")
    builder.button(text=" Оставить отзыв", callback_data="leave_feedback")
    builder.adjust(1)
    return builder.as_markup()