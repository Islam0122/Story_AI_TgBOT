import random

from gtts import gTTS
from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboard.inline import start_functions_keyboard, get_cancel_story_keyboard, return_menu_keyboard, \
    return_start_keyboard
from message_text.text import messages, button_texts, cancel, messages_text, photo_texts
from .start_functions import user_preferences
from .tale_ai_function import *
from filter.chat_types import ChatTypeFilter

tale_functions_private_router = Router()
tale_functions_private_router.message.filter(ChatTypeFilter(['private']))


class StoryState(StatesGroup):
    story_text = State()


# Запрос темы сказки
@tale_functions_private_router.callback_query(F.data == "create_story")
async def story(query: types.CallbackQuery, state: FSMContext) -> None:
    user_id = query.from_user.id
    language = user_preferences.get(user_id, {}).get('language', 'ru')  # Получаем предпочитаемый язык пользователя
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text=messages_text['by_text'][language], callback_data='create_story_by_text'))
    keyboard.add(InlineKeyboardButton(text=messages_text['by_photo'][language], callback_data='create_story_by_photo'))
    keyboard.add(InlineKeyboardButton(text=messages[language]['return_menu'], callback_data='start_'))
    await query.message.edit_caption(
        caption=messages_text['choose_method'][language],
        reply_markup=keyboard.adjust(1).as_markup()
    )


@tale_functions_private_router.callback_query(F.data.startswith("create_story_by_text"))
async def create_story_by_text(query: types.CallbackQuery, state: FSMContext) -> None:
    user_id = query.from_user.id
    language = user_preferences.get(user_id, {}).get('language', 'ru')
    await query.message.edit_caption(caption=messages[language]["ask_theme"],
                                     reply_markup=get_cancel_story_keyboard(language))
    await state.set_state(StoryState.story_text)


@tale_functions_private_router.callback_query(F.data == "cancel_create_story")
async def cancel_create_story(query: types.CallbackQuery, state: FSMContext) -> None:
    user_id = query.from_user.id
    language = user_preferences.get(user_id, {}).get('language', 'ru')  # Язык пользователя
    await state.clear()
    await query.message.edit_caption(caption=messages[language]['story_canceled'],
                                     reply_markup=start_functions_keyboard(language))


@tale_functions_private_router.callback_query(F.data == "cancel_story")
async def cancel_create_story(query: types.CallbackQuery, state: FSMContext) -> None:
    await query.message.delete()
    user_id = query.from_user.id
    language = user_preferences.get(user_id, {}).get('language', 'ru')  # Язык пользователя
    await state.clear()
    photo_path = 'media/welcome_img.jpg'
    await query.message.answer_photo(
        photo=types.FSInputFile(photo_path),
        caption=messages[language]['story_canceled'],
        reply_markup=start_functions_keyboard(language))


# Обработка введенной темы сказки
@tale_functions_private_router.message(StoryState.story_text)
async def process_story_text(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    language = user_preferences.get(user_id, {}).get('language', 'ru')  # Язык пользователя
    if message.text:
        story_theme = message.text
        keyboard = InlineKeyboardBuilder()
        keyboard.add(InlineKeyboardButton(text=messages[language]['listen'], callback_data='listen'))
        keyboard.add(InlineKeyboardButton(text=messages[language]['return_menu'], callback_data='start_'))
        generated_story = sent_prompt_and_get_response(story_theme, language)
        await message.answer(text=generated_story, reply_markup=keyboard.adjust(1).as_markup())
        await state.clear()
    elif message.photo:
        keyboard = InlineKeyboardBuilder()
        keyboard.add(InlineKeyboardButton(text=messages[language]['listen'], callback_data='listen'))
        keyboard.add(InlineKeyboardButton(text=messages[language]['return_menu'], callback_data='start_'))
        # generated_story_by_photo =
        await message.answer(text=f"it is photo", reply_markup=keyboard.adjust(1).as_markup())
        await state.clear()
    else:
        keyboard = InlineKeyboardBuilder()
        keyboard.add(InlineKeyboardButton(text=cancel[language], callback_data="cancel_story"))
        await message.answer(messages[language]["request_canceled_story"], reply_markup=keyboard.adjust(1).as_markup())


@tale_functions_private_router.callback_query(F.data.startswith("create_story_by_photo"))
async def create_story_by_photo(query: types.CallbackQuery, state: FSMContext) -> None:
    user_id = query.from_user.id
    language = user_preferences.get(user_id, {}).get('language', 'ru')

    # Отправляем сообщение с текстом на выбранном языке
    await query.message.edit_caption(
        caption=photo_texts['send_photo'][language],
        reply_markup=get_cancel_story_keyboard(language)
    )

    # Устанавливаем состояние для дальнейших шагов
    await state.set_state(StoryState.story_text)



@tale_functions_private_router.callback_query(F.data.startswith("view_top_stories"))
async def view_top_stories(query: types.CallbackQuery, state: FSMContext) -> None:
    user_id = query.from_user.id
    language = user_preferences.get(user_id, {}).get('language', 'ru')
    if language == 'en':
        topics = [
            "Путешествие во времени",
            "Мифы и легенды",
            "Инопланетные цивилизации",
            "Секретные агенты",
            "Таинственные исчезновения",
            "Герои и суперспособности",
            "Открытия великих учёных",
            "Космические экспедиции",
            "Городские легенды и страшилки",
            "Философские притчи"
        ]
    else:
        topics = [
            "Time Travel Adventures",
            "Myths and Legends",
            "Alien Civilizations",
            "Secret Agents",
            "Mysterious Disappearances",
            "Heroes and Superpowers",
            "Great Scientific Discoveries",
            "Space Expeditions",
            "Urban Legends and Ghost Stories",
            "Philosophical Parables"
        ]

    top_3_stories = random.choices(topics, k=3)  # С выбором с повторениями, если важно

    for story in top_3_stories:
        generated_story = sent_prompt_and_get_response(story, language)
        keyboard = InlineKeyboardBuilder()
        keyboard.add(InlineKeyboardButton(text=messages[language]['listen'], callback_data='listen'))
        await query.message.answer(text=generated_story, reply_markup=keyboard.adjust(1).as_markup())

    # Финальное сообщение с кнопкой
    await query.message.answer(messages[language]['top_story'], reply_markup=return_start_keyboard(language))


@tale_functions_private_router.callback_query(F.data.startswith("listen"))
async def listen_story(query: types.CallbackQuery, state: FSMContext) -> None:
    text = query.message.text
    user_id = query.from_user.id
    language = user_preferences.get(user_id, {}).get('language', 'ru')
    await query.message.edit_text(text, reply_markup=return_start_keyboard(language))
    wait_messages = {
        'ru': "Пожалуйста, подождите до трёх минут. Генерируется голос...",
        'en': "Please wait up to three minutes. Generating voice...",
        'kgz': "Үч мүнөткө чейин күтүп туруңуз. Үн түзүлүүдө..."
    }
    wait_message = wait_messages.get(language, wait_messages['ru'])
    await query.message.answer(wait_message)

    lang_code = 'en' if language == 'en' else 'ru'
    tts = gTTS(text=text, lang=lang_code)

    # Сохраняем аудиофайл
    file_path = f"{user_id}.mp3"
    tts.save(file_path)
    voice = types.FSInputFile(file_path)

    await query.message.answer_voice(voice)

    # Удаляем файл после отправки
    os.remove(file_path)
