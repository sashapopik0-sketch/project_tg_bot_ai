"""
Модуль взаимодействия с OpenAI-совместимым API для генерации текстовых ответов.

Реализует асинхронную функцию отправки запросов к языковой модели
с поддержкой сохранения истории сообщений в рамках сессии.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client: OpenAI = OpenAI(api_key=os.getenv('AI_KEY'), base_url=os.getenv('BASE_URL'))

async def generate_text_response(text: str) -> str:
    """Генерирует текстовый ответ на основе переданного сообщения пользователя.

    :param text: Текст сообщения для отправки в языковую модель.
    :type text: str
    :returns: Сгенерированный ответ модели или строка с описанием ошибки.
    :rtype: str
    :raises Exception: В случае сетевых сбоев или ошибок валидации API.
    """
    messages: list[dict[str, str]] = [
    {
        "role": "system",
        "content": "Ты помощник, который отвечает, запоминает, помогает на разные сообщения"
    }
    ]

    messages.append(
        {
            "role": "user",
            "content": text
        }
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=700
    )

    ai_reply = response.choices[0].message.content
    messages.append(
        {
            "role": "assistant",
            "content": ai_reply
        }
    )

    return ai_reply