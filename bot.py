from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
from aiogram.types import Message
from aiogram import Router
from deep_translator import GoogleTranslator
import asyncio

API_TOKEN = "7974964771:AAHi9YAJo-i9ss9vueZ1BowJTAEFTF5o6Ig"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

LANGS = {"ru": "Русский", "en": "Английский", "de": "Немецкий",
         "es": "Испанский", "ja": "Японский"}

@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Привет! Я бот-переводчик.\n"
        "Формат: <откуда> <куда> текст\n"
        "Коды языков: ru en de es ja\n\n"
        "Пример:\nru en Привет\nen es Hello"
    )

@router.message()
async def translate(message: Message):
    try:
        parts = message.text.split(" ", 3)
        if len(parts) < 3:
            await message.answer("Неверный формат. Пример: ru en Привет")
            return

        src, dest, text = parts[0], parts[1], " ".join(parts[2:])
        if src not in LANGS or dest not in LANGS:
            await message.answer("Доступные языки: ru en de es ja")
            return

        translated = GoogleTranslator(source=src, target=dest).translate(text)

        await message.answer(f"Перевод ({LANGS[src]} → {LANGS[dest]}):\n{translated}")

    except Exception as e:
        await message.answer(f"Ошибка: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
