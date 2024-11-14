from aiogram.types import InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder
from message_text.text import button_texts,messages,cancel


def start_functions_keyboard(language):
    """Функция для создания основной клавиатуры с кнопками действий на выбранном языке."""
    keyboard = InlineKeyboardBuilder()

    # Получаем нужные тексты кнопок на основе выбранного языка
    texts = button_texts.get(language)

    # Создаем кнопки
    keyboard.add(InlineKeyboardButton(text=texts['create_story'], callback_data='create_story'))
    keyboard.add(InlineKeyboardButton(text=texts['view_top_stories'], callback_data='view_top_stories'))

    keyboard.add(InlineKeyboardButton(text=texts['feedback'], callback_data='feedback'))

    keyboard.add(InlineKeyboardButton(text=texts['help'], callback_data='help'))
    keyboard.add(InlineKeyboardButton(text=texts['about'], callback_data='about'))

    keyboard.add(InlineKeyboardButton(text=texts['change_language'], callback_data='change_language'))

    keyboard.add(InlineKeyboardButton(text="Начать задание ", callback_data='chat_bot'))
    return keyboard.adjust(2, 1, 2, 1).as_markup()


def return_menu_from_help_keyboard(language):
    """Функция для создания основной клавиатуры с кнопками действий на выбранном языке."""
    keyboard = InlineKeyboardBuilder()

    # Получаем нужные тексты кнопок на основе выбранного языка
    texts = button_texts.get(language)

    # Создаем кнопки
    keyboard.add(InlineKeyboardButton(text=texts['create_story'], callback_data='create_story'))
    keyboard.add(InlineKeyboardButton(text=texts['view_top_stories'], callback_data='view_top_stories'))

    keyboard.add(InlineKeyboardButton(text=texts['feedback'], callback_data='feedback'))
    keyboard.add(InlineKeyboardButton(text=texts['about'], callback_data='about'))
    keyboard.add(InlineKeyboardButton(text=texts['change_language'], callback_data='change_language'))
    keyboard.add(InlineKeyboardButton(text=texts['return_menu'], callback_data='start'))
    return keyboard.adjust(2, 1, 2, 1).as_markup()


def return_menu_keyboard(language):
    """Функция для создания клавиатуры с кнопкой 'Вернуться в меню'."""
    texts = button_texts.get(language, button_texts['ru'])  # По умолчанию русский
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text=texts['return_menu'], callback_data='start'))
    return keyboard.as_markup()


def return_start_keyboard(language):
    """Функция для создания клавиатуры с кнопкой 'Вернуться в меню'."""
    texts = button_texts.get(language, button_texts['ru'])  # По умолчанию русский
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text=texts['return_menu'], callback_data='start_'))
    return keyboard.as_markup()


def return_menu_from_about_keyboard(language):
    """Функция для создания клавиатуры с кнопкой 'Вернуться в меню'."""
    texts = button_texts.get(language, button_texts['ru'])  # По умолчанию русский
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text=texts['feedback'], callback_data='feedback'))
    keyboard.add(InlineKeyboardButton(text=texts['return_menu'], callback_data='start'))
    return keyboard.adjust(1,1).as_markup()


def language_selection_keyboard(language: str):
    """Функция для создания клавиатуры выбора языка."""
    texts = button_texts.get(language, button_texts['ru'])  # По умолчанию русский
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_language_ru"),
        InlineKeyboardButton(text="🇬🇧 English", callback_data="set_language_en"),
        InlineKeyboardButton(text="🇰🇬 Кыргызча", callback_data="set_language_kgz"),
        InlineKeyboardButton(text=texts['return_menu'], callback_data='start'))

    return keyboard.adjust(3).as_markup()


def get_cancel_keyboard(language):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text=cancel[language], callback_data="cancel_feedback"))
    return keyboard.as_markup()


def get_cancel_story_keyboard(language):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text=cancel[language], callback_data="cancel_create_story"))
    return keyboard.adjust(1).as_markup()

