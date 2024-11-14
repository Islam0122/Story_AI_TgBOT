import random
from aiogram.filters import CommandStart, Command
from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .tale_ai_function import *
from filter.chat_types import ChatTypeFilter

chat_bot_functions_private_router = Router()
chat_bot_functions_private_router.message.filter(ChatTypeFilter(['private']))


class SituationState(StatesGroup):
    question = State()
    text = State()


db_list = [
    {
        "id": 1,
        "text": "Вы опоздали на важную встречу. Как вы поступите: извинитесь и объясните причины или постараетесь скрыть опоздание?",
        "keywords": ["опоздание", "извинения", "честность", "объяснение"]
    },
    {
        "id": 2,
        "text": "Вы нашли кошелек с деньгами на улице. Что вы сделаете: оставите его себе или отдадите в полицию?",
        "keywords": ["честность", "добродетель", "выбор", "поступок"]
    },
    {
        "id": 3,
        "text": "Вам предложили работу с более высокой зарплатой, но она в другом городе. Вы готовы к переезду или предпочтете остаться на текущем месте?",
        "keywords": ["карьера", "переезд", "риски", "работа"]
    },
    {
        "id": 4,
        "text": "Ваш лучший друг попросил вас помочь ему скрыть ошибку, которая может повлиять на его карьеру. Как поступите?",
        "keywords": ["дружба", "честность", "поступок", "выбор"]
    },
    {
        "id": 5,
        "text": "Ваша семья сталкивается с финансовыми трудностями. Как вы будете действовать: возьмете кредит или постараетесь решить проблему без заемных средств?",
        "keywords": ["финансы", "долг", "семья", "кредит"]
    },
    {
        "id": 6,
        "text": "Вам предлагают стать волонтером в благотворительной организации. Какие причины будут для вас важны, чтобы согласиться?",
        "keywords": ["добровольчество", "помощь", "благотворительность", "причины"]
    },
    {
        "id": 7,
        "text": "Вас пригласили на вечер, но вы устали после долгого рабочего дня. Как вы поступите: пойдете на встречу или останетесь дома?",
        "keywords": ["усталость", "общение", "решение", "выбор"]
    },
    {
        "id": 8,
        "text": "Вы стали свидетелем несправедливого поступка на работе. Как вы поступите: вмешаетесь или оставите все как есть?",
        "keywords": ["несправедливость", "решение", "работа", "поступок"]
    },
    {
        "id": 9,
        "text": "Ваш коллега попросил вас одолжить деньги, но вы не уверены, что он вернет долг. Что вы решите?",
        "keywords": ["финансовая помощь", "долг", "дружба", "риски"]
    },
    {
        "id": 10,
        "text": "Вы узнаете, что ваш знакомый оказался в сложной ситуации. Как вы поступите: предложите помощь или оставите все как есть?",
        "keywords": ["дружба", "помощь", "выбор", "реакция"]
    }
]


@chat_bot_functions_private_router.message(Command("start_chat_bot"))
async def start_chat_bot(message: types.Message):
    await message.reply(
        "Привет! Я — бот для оценки твоих действий в разных ситуациях. Напиши /situation, чтобы получить новое задание.")


@chat_bot_functions_private_router.callback_query(F.data.startswith('chat_bot'))
async def chat_bot_callback(query: types.CallbackQuery):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='start'))
    await query.message.edit_caption(
        caption="Привет! Я — бот для оценки твоих действий в разных ситуациях. Напиши /situation, чтобы получить "
                "новое задание.",
        reply_markup=keyboard.as_markup(), )


@chat_bot_functions_private_router.message(Command("situation"))
async def situation_(message: types.Message, state: FSMContext):
    situation = random.choice(db_list)
    question = situation['text']
    await message.reply(question)
    await state.update_data(question=question, keywords=situation['keywords'])
    await state.set_state(SituationState.text)


@chat_bot_functions_private_router.message(F.text == "Отмена")
async def cancel_chat_bot(message: types.Message, state: FSMContext):
    await state.clear()
    await message.reply("Диалог отменен. Напиши /situation, чтобы начать заново.")


# Processing the user's answer
@chat_bot_functions_private_router.message(SituationState.text)
async def text_processing(message: types.Message, state: FSMContext):
    if message.text:
        data = await state.get_data()
        question = data['question']
        keywords = data['keywords']
        student_answer = message.text.lower()

        result = check_answer_get_response(question, keywords, student_answer)

        await message.reply(result)
        await state.clear()
        await message.reply("Напиши /situation, чтобы получить новое задание.")
    else:
        await message.reply("Пожалуйста, введите ответ на вопрос.")
