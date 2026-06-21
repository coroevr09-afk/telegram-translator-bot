import os 
import asyncio
from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from deep_translator import GoogleTranslator
from aiohttp import web  # Импортируем для фейкового веб-сервера

API_TOKEN = "7974964771:AAHi9YAJo-i9ss9vueZ1BowJTAEFTF5o6Ig"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

LANGS = {
    "ru": "🇷🇺 Русский",
    "en": "🇬🇧 Английский",
    "de": "🇩🇪 Немецкий",
    "es": "🇪🇸 Испанский",
    "ja": "🇯🇵 Японский"
}

user_target_lang = {}

def language_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=name, callback_data=code)]
            for code, name in LANGS.items()
        ]
    )

def change_lang_button():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔁 Сменить язык",
                    callback_data="change_lang"
                )
            ]
        ]
    )

@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "🌍 Выбери язык, НА КОТОРЫЙ переводить:",
        reply_markup=language_keyboard()
    )

@router.callback_query(F.data.in_(LANGS.keys()))
async def choose_language(callback):
    user_target_lang[callback.from_user.id] = callback.data
    await callback.message.answer(
        f"✅ Выбран язык: {LANGS[callback.data]}\n\n"
        "Теперь отправь текст — я сам определю язык"
    )
    await callback.answer()

@router.callback_query(F.data == "change_lang")
async def change_lang(callback):
    await callback.message.answer(
        "🌍 Выбери новый язык:",
        reply_markup=language_keyboard()
    )
    await callback.answer()

@router.message()
async def translate(message: Message):
    user_id = message.from_user.id

    if user_id not in user_target_lang:
        await message.answer(
            "Сначала выбери язык 👇",
            reply_markup=language_keyboard()
        )
        return

    target_lang = user_target_lang[user_id]

    try:
        translated = GoogleTranslator(
            source="auto",
            target=target_lang
        ).translate(message.text)

        await message.answer(
            f"Перевод на {LANGS[target_lang]}:\n\n{translated}",
            reply_markup=change_lang_button()
        )

    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")


async def handle(request):
    return web.Response(text="Bot is running smoothly!")

async def main():
  
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    
   
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

  
    await dp.start_polling(bot)

if __name__ == "main":  
    asyncio.run(main())