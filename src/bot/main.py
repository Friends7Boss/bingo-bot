# bot/main.py
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from database.db import init_db, get_session
from database.models import User
import secrets
import asyncio

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set in environment")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Ensure DB tables exist
init_db()

def create_referral_code():
    return secrets.token_hex(6)

async def get_or_create_user(telegram_id: str, phone_number: str | None = None):
    # Use blocking DB inside a thread to avoid blocking event loop
    def _db_work():
        session = get_session()
        try:
            user = session.query(User).filter(User.telegram_id == str(telegram_id)).first()
            if user:
                return user.id
            # create new user
            user = User(telegram_id=str(telegram_id), phone_number=phone_number, referral_code=create_referral_code())
            session.add(user)
            session.commit()
            return user.id
        finally:
            session.close()

    user_id = await asyncio.to_thread(_db_work)
    return user_id

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    # handle start with optional referral code: /start <code>
    parts = message.get_command(pure=True).split()
    # aiogram CommandStart doesn't pass args; check message.text
    args = message.text.split()
    ref_code = None
    if len(args) > 1:
        ref_code = args[1]

    await message.answer("Welcome to Bingo Bot! Please share your phone number using the Telegram contact button or type it now.")
    # create or ensure user
    await get_or_create_user(message.from_user.id)

@dp.message(Command(commands=["setphone"]))
async def setphone(message: types.Message):
    # user sends: /setphone 0912345678
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.reply("Usage: /setphone 0912345678")
        return
    phone = parts[1].strip()
    def _db_setphone():
        session = get_session()
        try:
            user = session.query(User).filter(User.telegram_id == str(message.from_user.id)).first()
            if not user:
                user = User(telegram_id=str(message.from_user.id), phone_number=phone, referral_code=create_referral_code())
                session.add(user)
            else:
                user.phone_number = phone
            session.commit()
            return True
        finally:
            session.close()
    ok = await asyncio.to_thread(_db_setphone)
    if ok:
        await message.reply(f"Phone updated to {phone}. Your referral link: t.me/{(await bot.get_me()).username}?start={message.from_user.id}")

@dp.message(Command(commands=["balance"]))
async def balance(message: types.Message):
    def _db_balance():
        session = get_session()
        try:
            user = session.query(User).filter(User.telegram_id == str(message.from_user.id)).first()
            if not user:
                return None
            return float(user.balance or 0)
        finally:
            session.close()
    bal = await asyncio.to_thread(_db_balance)
    if bal is None:
        await message.reply("No account found. Send /start to register.")
    else:
        await message.reply(f"Your balance: {bal} birr")

async def main():
    # start polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
