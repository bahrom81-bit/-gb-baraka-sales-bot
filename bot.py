import os
import json
import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://bahrom81-bit.github.io/gb-baraka-kalkulyator/")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable kerak")

bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
ORDERS_FILE = "orders.json"

PLENKA_TEXT = '''💥 <b>OPTOM POLIETILEN PLYONKA NARXLARI</b>
📅 <b>25.05.2026 holatiga ko‘ra</b>
📐 Ochilganda 3 m va 4 m

⏺ <b>Oq oliy nav</b> — 23 000 so‘m
⏺ <b>Qora</b> — 14 000 so‘m
⏺ <b>Ko‘k 6 m</b> — 19 000 so‘m
⏺ <b>Ko‘k 8 m</b> — 20 000 so‘m
⏺ <b>Qora 6 m</b> — 18 000 so‘m
⏺ <b>Qora 8 m</b> — 19 000 so‘m
⏺ <b>Oq 6 m</b> — 26 000 so‘m
⏺ <b>Ko‘k 10 m</b> — 35 000 so‘m

➕ <b>Qo‘shimcha:</b>
🇨🇳 <b>Xitoy EVA 8–16 m</b> — 34 200 so‘m
🇺🇿 <b>O‘zbekiston 8–16 m</b> — 29 400 so‘m

🌾 <b>Agro segment uchun oq plyonka</b>
➡️ 28 000 so‘mdan boshlanadi

📦 Ulgurji savdo
🚚 Respublika bo‘ylab yetkazib berish'''

SOYA_TEXT = '''🌤 <b>SOYA SETKA NARXLARI</b>
📦 100 metr rulon uchun

<b>95% soya setka</b>
⏺ 2 m — 1 032 000 so‘m
⏺ 3 m — 1 548 000 so‘m
⏺ 4 m — 2 064 000 so‘m
⏺ 5 m — 2 580 000 so‘m
⏺ 6 m — 3 096 000 so‘m
⏺ 8 m — 4 128 000 so‘m

<b>75% soya setka</b>
⏺ 2 m — 552 000 so‘m
⏺ 3 m — 828 000 so‘m
⏺ 4 m — 1 104 000 so‘m
⏺ 5 m — 1 380 000 so‘m
⏺ 6 m — 1 656 000 so‘m
⏺ 8 m — 2 208 000 so‘m'''

MOSKIT_TEXT = '''🪟 <b>MOSKIT SETKA NARXLARI</b>

⏺ <b>Kapron moskit setka</b>
📦 Rulonda 50 metr
💰 1 rulon — 130 000 so‘m

⏺ <b>Akfa moskit setka</b>
📦 Rulonda 30 metr
💰 1 rulon — 310 000 so‘m'''

CONTACT_TEXT = '''📩 <b>Buyurtma uchun:</b>
👉 @gb_baraka

📱 77 041 77 55
📱 90 048 77 55

📍 Toshkent Shahri, Uchtepa tumani,
O‘rikzor Qurilish bozori, J blok'''

def save_order(user, text):
    orders = []
    if os.path.exists(ORDERS_FILE):
        try:
            with open(ORDERS_FILE, "r", encoding="utf-8") as f:
                orders = json.load(f)
        except Exception:
            orders = []
    orders.append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_id": user.id,
        "username": user.username,
        "name": user.full_name,
        "text": text
    })
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)

def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧮 Narx kalkulyatori", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton(text="💰 Narx katalogi", callback_data="catalog")],
        [InlineKeyboardButton(text="📦 Buyurtma qabul qilish", callback_data="order")],
        [InlineKeyboardButton(text="📞 Aloqa", callback_data="contact")]
    ])

def catalog_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💥 Plyonka narxlari", callback_data="price_plyonka")],
        [InlineKeyboardButton(text="🌤 Soya setka narxlari", callback_data="price_soya")],
        [InlineKeyboardButton(text="🪟 Moskit setka narxlari", callback_data="price_moskit")],
        [InlineKeyboardButton(text="🧮 Kalkulyatorni ochish", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton(text="⬅️ Bosh menyu", callback_data="home")]
    ])

def back_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Narx katalogi", callback_data="catalog")],
        [InlineKeyboardButton(text="🏠 Bosh menyu", callback_data="home")]
    ])

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Assalomu alaykum! 👋\n\n"
        "🇺🇿 <b>GB BARAKA</b> rasmiy botiga xush kelibsiz!\n\n"
        "Bu bot orqali siz:\n"
        "🧮 plyonka narx kalkulyatoridan foydalanasiz\n"
        "💰 mahsulot narxlarini ko‘rasiz\n"
        "📦 buyurtma qoldirasiz\n"
        "📞 operator bilan bog‘lanasiz\n\n"
        "👇 Kerakli bo‘limni tanlang:",
        reply_markup=main_menu()
    )

@dp.callback_query(F.data == "home")
async def home(call: CallbackQuery):
    await call.message.edit_text("🏠 <b>Bosh menyu</b>\n\nKerakli bo‘limni tanlang:", reply_markup=main_menu())

@dp.callback_query(F.data == "catalog")
async def catalog(call: CallbackQuery):
    await call.message.edit_text("💰 <b>NARX KATALOGI</b>\n\nMahsulot turini tanlang:", reply_markup=catalog_menu())

@dp.callback_query(F.data == "price_plyonka")
async def price_plyonka(call: CallbackQuery):
    await call.message.edit_text(PLENKA_TEXT, reply_markup=back_menu())

@dp.callback_query(F.data == "price_soya")
async def price_soya(call: CallbackQuery):
    await call.message.edit_text(SOYA_TEXT, reply_markup=back_menu())

@dp.callback_query(F.data == "price_moskit")
async def price_moskit(call: CallbackQuery):
    await call.message.edit_text(MOSKIT_TEXT, reply_markup=back_menu())

@dp.callback_query(F.data == "contact")
async def contact(call: CallbackQuery):
    await call.message.edit_text(CONTACT_TEXT, reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📩 Telegram orqali yozish", url="https://t.me/gb_baraka")],
        [InlineKeyboardButton(text="🏠 Bosh menyu", callback_data="home")]
    ]))

@dp.callback_query(F.data == "order")
async def order(call: CallbackQuery):
    await call.message.edit_text(
        "📦 <b>Buyurtma qabul qilish</b>\n\n"
        "Buyurtma yozish uchun quyidagi shaklda xabar yuboring:\n\n"
        "<code>Buyurtma: oq plyonka 6 m, 2 rulon, telefon: 90...</code>\n\n"
        "Yoki kalkulyator orqali hisoblab, “Buyurtma berish” tugmasini bosing.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🧮 Kalkulyatorni ochish", web_app=WebAppInfo(url=WEBAPP_URL))],
            [InlineKeyboardButton(text="🏠 Bosh menyu", callback_data="home")]
        ])
    )

@dp.message(F.web_app_data)
async def webapp_order(message: Message):
    data = message.web_app_data.data
    save_order(message.from_user, data)
    await message.answer(
        "✅ <b>Hisob-kitob qabul qilindi!</b>\n\n"
        f"<pre>{data}</pre>\n\n"
        "📞 Operator tez orada bog‘lanadi.\n"
        "77 041 77 55 | 90 048 77 55"
    )
    if ADMIN_ID:
        await bot.send_message(ADMIN_ID, f"🆕 <b>Yangi hisob-kitob:</b>\n\n👤 {message.from_user.full_name}\n@{message.from_user.username}\n\n<pre>{data}</pre>")

@dp.message(F.text.regexp(r"(?i)^buyurtma"))
async def manual_order(message: Message):
    save_order(message.from_user, message.text)
    await message.answer("✅ Buyurtmangiz qabul qilindi.\nTez orada siz bilan bog‘lanamiz.\n\n📞 77 041 77 55\n📞 90 048 77 55")
    if ADMIN_ID:
        await bot.send_message(ADMIN_ID, f"🆕 <b>Yangi buyurtma:</b>\n\n👤 {message.from_user.full_name}\n@{message.from_user.username}\n\n{message.text}")

@dp.message(Command("admin"))
async def admin(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("Bu bo‘lim faqat admin uchun.")
        return
    count = 0
    if os.path.exists(ORDERS_FILE):
        try:
            with open(ORDERS_FILE, "r", encoding="utf-8") as f:
                count = len(json.load(f))
        except Exception:
            count = 0
    await message.answer(f"👨‍💼 <b>Admin panel</b>\n\n📦 Jami buyurtmalar: <b>{count}</b>\n\nBuyurtmalar <code>orders.json</code> faylida saqlanadi.")

@dp.message()
async def auto_reply(message: Message):
    await message.answer(
        "Savolingiz uchun rahmat ✅\n\n"
        "Kerakli bo‘limni tanlang yoki buyurtmani quyidagicha yozing:\n"
        "<code>Buyurtma: oq plyonka 6 m, 2 rulon</code>",
        reply_markup=main_menu()
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
