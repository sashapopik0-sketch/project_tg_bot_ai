"""
Модуль для генерации аудио (Text-to-Speech) с использованием OpenAI-совместимого API.

Преобразует переданный текст в аудиофайл формата WAV и возвращает объект,
совместимый с методами отправки сообщений aiogram.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
from aiogram.types import BufferedInputFile

load_dotenv()

client: OpenAI = OpenAI(api_key=os.getenv('AI_KEY'), base_url=os.getenv('BASE_URL'))


async def generate_audio_response(text: str):
    """Генерирует аудиофайл из текстовой строки с помощью TTS-модели.

    :param text: Текст, который необходимо преобразовать в речь.
    :type text: str
    :returns: Готовый к отправке аудиофайл в формате WAV.
    :rtype: aiogram.types.BufferedInputFile
    """
    response = client.audio.speech.create(
        model="canopylabs/orpheus-v1-english",
        input=text,
        voice="troy",
        response_format="wav"
    )

    audio_bytes = await response.aread()
        
    return BufferedInputFile(
        file=audio_bytes,
        filename="voice.wav"
    )
