from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from data.quiz_data import WELCOME_TEXT, ADOPTION_TEXT
from keyboards.main import get_start_keyboard, get_back_to_start_keyboard

# Создаем роутер
router = Router()


# 1. Обработчик команды /start
@router.message(CommandStart())
async def cmd_start(message: Message):
    """Отправляет приветственное сообщение и стартовую клавиатуру."""
    await message.answer(
        WELCOME_TEXT,
        reply_markup=get_start_keyboard(),
        parse_mode="HTML" # Нужно, чтобы работали теги <b> и <a> в тексте
    )


# 2. Обработчик нажатия на кнопку "О программе опеки"
@router.callback_query(F.data == "about_adoption")
async def cb_about_adoption(callback: CallbackQuery):
    """Редактирует сообщение и показывает текст об опеке."""
    await callback.message.edit_text(
        ADOPTION_TEXT,
        reply_markup=get_back_to_start_keyboard(),
        parse_mode="HTML"
    )
    # Обязательно отвечаем на callback, чтобы убрать "часики" загрузки в Telegram
    await callback.answer()


# 3. Обработчик нажатия на кнопку "В главное меню"
@router.callback_query(F.data == "back_to_start")
async def cb_back_to_start(callback: CallbackQuery):
    """Возвращает пользователя к стартовому сообщению."""
    await callback.message.edit_text(
        WELCOME_TEXT,
        reply_markup=get_start_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()