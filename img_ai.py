"""
Модуль для анализа изображений с использованием OpenAI-совместимого API.

Обеспечивает взаимодействие с Vision API для анализа изображений,
передаваемых в формате base64, и генерации текстовых ответов на основе запроса.
"""

import os
import base64
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client: OpenAI = OpenAI(api_key=os.getenv('AI_KEY'), base_url=os.getenv('BASE_URL'))


async def generate_image_response(base64_image: str, text: str = "Опиши подробно фото") -> str | None:
    """Генерирует текстовое описание или ответ на вопрос по содержимому изображения.

    Отправляет запрос к мультимодальной модели, содержащий изображение в кодировке base64
    и текстовую инструкцию, после чего возвращает ответ модели.

    :param base64_image: Строковое представление изображения в кодировке base64.
    :type base64_image: str
    :param text: Текстовый запрос или подсказка для модели.
    :type text: str
    :returns: Строка с ответом модели, содержащая анализ изображения.
    :rtype: str
    """
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text", "text": text
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
        model="meta-llama/llama-4-scout-17b-16e-instruct",
    )
    return chat_completion.choices[0].message.content
