# 🤖 AI Telegram Bot с мультимодальными возможностями

**Умный Telegram бот** с поддержкой **текста, изображений, аудио и голосовых сообщений**. Анализирует фото, транскрибирует аудио, отвечает на вопросы.

## ✨ Возможности

| Функция | Описание | ✅ Статус |
|---------|----------|----------|
| **💬 Текст** | Обработка текстовых сообщений | ✅ |
| **🖼️ Изображения** | Анализ и описание фото | ✅ |
| **🎤 Голосовые** | Транскрипция голосовых сообщений | ✅ |
| **🎵 Аудио** | Транскрипция аудиофайлов | ✅ |
| **⚙️ Таймауты** | Обработка больших файлов | ✅ |

## 🚀 Быстрый старт

### 1. Клонируй проект
```bash
git clone <твой-репозиторий>
cd ai-telegram-bot
```

### 2. Установи зависимости
```bash
pip install -r requirements.txt
```

### 3. Создай `.env`
```env
BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_key
```

### 4. Запусти
```bash
python bot.py
```

## 🛠 Структура проекта

```
📦 project/
 ├── 📄 bot.py              # Точка входа, роутеры, FSM, обработка команд и медиа
 ├── 📄 text_ai.py          # Генерация текстовых ответов (LLM)
 ├── 📄 img_ai.py           # Анализ изображений (Vision API)
 ├── 📄 audio_ai.py         # Генерация аудио (TTS)
 ├── 📄 requirements.txt    # Python-зависимости
 └── 📄 .env                # Секретные ключи (не коммитить в Git!)
```

## 🔧 Основной код (`bot.py`)

```python
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

bot = Bot(
    token=os.getenv("BOT_TOKEN"),
    default=DefaultBotProperties(timeout=60)
)
dp = Dispatcher()

# Регистрация обработчиков
from handlers import text, image, audio

# Запуск
async def main():
    await dp.start_polling(bot, timeout=60)

if __name__ == "__main__":
    asyncio.run(main())
```

## ⚙️ Конфигурация

### `.env`
```env
# Telegram
BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11

# OpenAI (или другой LLM)
OPENAI_API_KEY=sk-proj-xxx...
```

## 📄 requirements.txt

```txt
aiogram==3.13.1
openai==1.51.0
python-dotenv==1.0.1
pydub==0.25.1
aiohttp==3.10.10
```

## 📄 Лицензия

MIT License — используй на здоровье! 🚀

***

**Сделано с ❤️ для AI разработчиков**  
**Автор:** Sasha Popik  

***
