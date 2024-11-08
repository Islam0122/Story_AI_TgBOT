from aiogram import F, types, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from filter.chat_types import ChatTypeFilter
from keyboard.inline import *
from message_text.text import messages

start_functions_private_router = Router()
start_functions_private_router.message.filter(ChatTypeFilter(['private']))

user_preferences = {}


async def send_welcome_message(user, target):
    """Функция для отправки приветственного сообщения с фото."""
    user_id = user.id
    if user_id not in user_preferences:
        user_preferences[user_id] = {'language': 'ru'}

    language = user_preferences[user_id]['language']
    photo_path = 'media/welcome_img.jpg'
    keyboard_markup = start_functions_keyboard(language)
    await target.answer_photo(
        photo=types.FSInputFile(photo_path),
        caption=f"{messages[language]['welcome'].format(user_name=user.full_name)}",
        reply_markup=keyboard_markup
    )


@start_functions_private_router.message(CommandStart())
@start_functions_private_router.message(F.text.lower() == 'start')
async def start_cmd(message: types.Message):
    """Обработчик команды /start"""
    await send_welcome_message(message.from_user, message)


@start_functions_private_router.callback_query(F.data.startswith('start_'))
async def start_command_callback_query(query: types.CallbackQuery) -> None:
    """Обработчик callback_query с командой start"""
    await query.message.delete()
    await send_welcome_message(query.from_user, query.message)


@start_functions_private_router.callback_query(F.data.startswith('start'))
async def start_command_callback_query(query: types.CallbackQuery) -> None:
    """Обработчик callback_query с командой start"""
    user_id = query.from_user.id
    if user_id not in user_preferences:
        user_preferences[user_id] = {'language': 'ru'}

    language = user_preferences[user_id]['language']
    keyboard_markup = start_functions_keyboard(language)

    await query.message.edit_caption(
        caption=messages[language]['about_message'],
        reply_markup=keyboard_markup,
        parse_mode=ParseMode.MARKDOWN
    )


@start_functions_private_router.callback_query(F.data.startswith('about'))
async def about_bot_callback(query: types.CallbackQuery):
    user_id = query.from_user.id
    if user_id not in user_preferences:
        user_preferences[user_id] = {'language': 'ru'}

    language = user_preferences[user_id]['language']
    await query.message.edit_caption(
        caption=messages[language]['about_message'],
        reply_markup=return_menu_from_about_keyboard(language),
        parse_mode=ParseMode.MARKDOWN)


@start_functions_private_router.callback_query(F.data.startswith('help'))
async def help_callback(query: types.CallbackQuery):
    user_id = query.from_user.id
    if user_id not in user_preferences:
        user_preferences[user_id] = {'language': 'ru'}

    language = user_preferences[user_id]['language']
    await query.message.edit_caption(
        caption=messages[language]['help_message'],
        reply_markup=return_menu_from_help_keyboard(language),
        parse_mode=ParseMode.MARKDOWN)


@start_functions_private_router.callback_query(F.data == 'change_language')
async def select_language_callback(query: types.CallbackQuery):
    """Обработчик выбора языка через callback"""
    user_id = query.from_user.id
    if user_id not in user_preferences:
        user_preferences[user_id] = {'language': 'ru'}

    language = user_preferences[user_id]['language']
    keyboard = language_selection_keyboard(language)
    await query.message.edit_caption(
        caption="Please select your language / Пожалуйста, выберите язык / Тилди тандаңыз:",
        reply_markup=keyboard
    )


@start_functions_private_router.callback_query(F.data.startswith('set_language_'))
async def set_language_callback(query: types.CallbackQuery):
    """Обработчик установки языка через callback"""
    user_id = query.from_user.id

    # Если пользователь не существует, инициализируем его настройки
    if user_id not in user_preferences:
        user_preferences[user_id] = {}

    # Установка языка в зависимости от нажатой кнопки
    if query.data == "set_language_ru":
        user_preferences[user_id]['language'] = 'ru'
        response = "Язык установлен на русский."
    elif query.data == "set_language_en":
        user_preferences[user_id]['language'] = 'en'
        response = "Language set to English."
    elif query.data == "set_language_kgz":
        user_preferences[user_id]['language'] = 'kgz'
        response = "Тил кыргызча болуп орнотулду."

    language = user_preferences[user_id]['language']
    await query.message.edit_caption(
        caption=response,
        reply_markup=start_functions_keyboard(language),
    )