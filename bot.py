"""
Основной модуль Telegram-бота на базе aiogram 3.

Реализует обработку команд, управление состояниями (FSM),
взаимодействие с пользователем и вызов внешних модулей
для генерации текста, анализа изображений и синтеза речи.
"""

import asyncio
import os
import base64
from aiogram import Router, Bot, Dispatcher, F
from aiogram.types import Message, PhotoSize
from aiogram.filters import Command
from img_ai import generate_image_response
from text_ai import generate_text_response
from audio_ai import generate_audio_response
from dotenv import load_dotenv
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

load_dotenv()

bot = Bot(token=os.getenv('BOT_KEY'))
router = Router()
storage = MemoryStorage()
db = Dispatcher(storage=storage)

class BotStates(StatesGroup):
    """Группа состояний конечного автомата (FSM) для управления режимами бота."""
    waiting_text = State()
    waiting_image = State()
    waiting_audio = State()

@router.message(Command("start"))
async def start_command(message: Message):
    """Обрабатывает команду /start. Отправляет приветственное сообщение со списком команд.

    :param message: Входящее сообщение от пользователя.
    :type message: aiogram.types.Message
    :returns: None
    :rtype: None
    """
    await message.answer(
"""🤖 Привет! Я AI-бот!

Команды:
/text — задать вопрос 
/image — анализ фото  
/audio — создание аудио по тексту
Как работает: /text → пиши вопрос → ответ!"""
                        )

@router.message(Command("text"))
async def cmd_text(message: Message, state: FSMContext):
    """Обрабатывает команду /text. Устанавливает состояние ожидания текстового запроса.

    :param message: Входящее сообщение.
    :type message: aiogram.types.Message
    :param state: Контекст конечного автомата.
    :type state: aiogram.fsm.context.FSMContext
    :returns: None
    :rtype: None
    """
    try:
        await message.answer("Задай мне любой вопрос, и я постараюсь ответить!")
        await state.set_state(BotStates.waiting_text)
    except Exception as e:
        print(f"Error in cmd_text: {e}")
        await message.answer("Произошла ошибка. Попробуйте еще раз.")

@router.message(BotStates.waiting_text)
async def text_command(message: Message, state: FSMContext):
    """Обрабатывает текстовый ввод пользователя в режиме ожидания текста.

    :param message: Входящее сообщение с текстом.
    :type message: aiogram.types.Message
    :param state: Контекст конечного автомата.
    :type state: aiogram.fsm.context.FSMContext
    :returns: None
    :rtype: None
    """
    try:
        answer = await generate_text_response(message.text)
        await message.answer(answer)
        await state.clear()
    except Exception as e:
        print(f"Error in text_command: {e}")
        await message.answer("Произошла ошибка. Попробуйте еще раз.")

@router.message(Command("image"))
async def cmd_image(message: Message, state: FSMContext):
    """Обрабатывает команду /image. Устанавливает состояние ожидания изображения.

    :param message: Входящее сообщение.
    :type message: aiogram.types.Message
    :param state: Контекст конечного автомата.
    :type state: aiogram.fsm.context.FSMContext
    :returns: None
    :rtype: None
    """
    await message.answer("Отправь мне изображение, и какое-нибудь вопрос")
    await state.set_state(BotStates.waiting_image)


@router.message(BotStates.waiting_image, F.photo)
async def image_command(message: Message, state: FSMContext):
    """Обрабатывает полученное изображение. Загружает файл, кодирует в base64 и отправляет на анализ.

    :param message: Входящее сообщение с фото.
    :type message: aiogram.types.Message
    :param state: Контекст конечного автомата.
    :type state: aiogram.fsm.context.FSMContext
    :returns: None
    :rtype: None
    """
    try:
        await message.answer("Анализирую...")
        photo: list[PhotoSize] | None = message.photo[-1]
        file_info = await bot.get_file(photo.file_id)

        for attempt in range(3):
            try:
                photo_bytes = await asyncio.wait_for(
                    bot.download_file(file_info.file_path),
                    timeout=30.0
                )
                break
            except asyncio.TimeoutError:
                if attempt == 2:
                    await message.answer("Изображение загружается слишком медленно")
                    return
                await asyncio.sleep(2)

        photo_bytes.seek(0)
        base64_image = base64.b64encode(photo_bytes.getvalue()).decode('utf-8')
        answer = await generate_image_response(base64_image, message.caption or "Опиши подробно фото")
            
        await message.answer(answer)
        await state.clear()
    except Exception as e:
        print(f"Error in image_command: {e}")
        await message.answer("Произошла ошибка. Попробуйте еще раз.")

@router.message(Command("audio"))
async def cmd_audio(message: Message, state: FSMContext):
    """Обрабатывает команду /audio. Устанавливает состояние ожидания текста для озвучки.

    :param message: Входящее сообщение.
    :type message: aiogram.types.Message
    :param state: Контекст конечного автомата.
    :type state: aiogram.fsm.context.FSMContext
    :returns: None
    :rtype: None
    """
    await message.answer("Отправь мне текст, и я создам аудио из него!")
    await state.set_state(BotStates.waiting_audio)

@router.message(BotStates.waiting_audio)
async def audio_command(message: Message, state: FSMContext):
    """Обрабатывает текстовый ввод пользователя в режиме ожидания аудио.

    :param message: Входящее сообщение с текстом.
    :type message: aiogram.types.Message
    :param state: Контекст конечного автомата.
    :type state: aiogram.fsm.context.FSMContext
    :returns: None
    :rtype: None
    """
    try:
        await message.answer("Создаю...")
        audio_file = await generate_audio_response(message.text)
        await message.answer_audio(audio_file)
        await state.clear()
    except Exception as e:
        print(f"Error in audio_command: {e}")
        await message.answer("Произошла ошибка. Попробуйте еще раз.")

async def main():
    """Инициализирует диспетчер, подключает роутер и запускает polling бота.

    :returns: None
    :rtype: None
    """
    print("Бот запущен...")
    db.include_router(router)
    await db.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен пользователем.")
