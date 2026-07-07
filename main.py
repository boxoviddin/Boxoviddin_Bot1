import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import BotCommand

# Token va Admin ID
TOKEN = "8215613212:AAEmwln_zfLBYazuYbzynqC0Fqg_uTQvr_k"
ADMIN_ID = 7575052801

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

class ComplaintState(StatesGroup):
    waiting_for_text = State()

# 1. "🛍 Mahsulotlar" tugmasiga bosilganda Inline WebApp tugmasini ko'rsatish
@dp.message(F.text == "🛍 Mahsulotlar")
async def show_products(message: types.Message):
    builder = InlineKeyboardBuilder()
    # O'z saytingiz yoki ilova manzilingizni shu yerga qo'ying
    builder.button(
        text="📱 Ilovani ochish", 
        web_app=types.WebAppInfo(url="https://google.com") 
    )
    await message.answer(
        "Mahsulotlarimiz bilan tanishish uchun pastdagi tugmani bosing:", 
        reply_markup=builder.as_markup()
    )

# 2. Start komandasi va asosiy menyu
@dp.message(CommandStart())
async def start_command(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="🛍 Mahsulotlar"))
    builder.add(types.KeyboardButton(text="ℹ️ Biz haqimizda"))
    builder.add(types.KeyboardButton(text="📞 Aloqa"))
    builder.add(types.KeyboardButton(text="📝 Shikoyatlar"))
    builder.adjust(2)

    await message.answer(
        f"Xush kelibsiz, {message.from_user.full_name}!",
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=False)
    )

# Boshqa handlerlar (o'zgarishsiz)
@dp.message(F.text == "📞 Aloqa")
async def contact_handler(message: types.Message):
    await message.answer("📞 Admin: @admin_username\nTelefon: +998886577553")

@dp.message(F.text == "ℹ️ Biz haqimizda")
async def about_us_handler(message: types.Message):
    await message.answer("Biz eng sifatli mahsulotlarni yetkazib beramiz!")

@dp.message(F.text == "📝 Shikoyatlar")
async def complaint_start(message: types.Message, state: FSMContext):
    await state.set_state(ComplaintState.waiting_for_text)
    await message.answer("Shikoyatingizni yozib yuboring:")

@dp.message(ComplaintState.waiting_for_text)
async def process_complaint(message: types.Message, state: FSMContext):
    await bot.send_message(ADMIN_ID, f"📩 Yangi xabar: {message.text}")
    await message.answer("✅ Yuborildi.")
    await state.clear()

async def main():
    # Menyu tugmalarini (Menu button) o'rnatish
    await bot.set_my_commands([BotCommand(command="start", description="Botni qayta ishga tushirish")])
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
