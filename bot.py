import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

TOKEN = "7693451512:AAHSDmLEj7aC9tykE9TQf5A0y8yj4irN5xQ"  # Вставь свой API-токен
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Подключение к базе данных
conn = sqlite3.connect("licenses.db")
cursor = conn.cursor()

# Создаем таблицу для ключей (если её нет)
cursor.execute('''CREATE TABLE IF NOT EXISTS licenses (key TEXT UNIQUE, active INTEGER DEFAULT 1)''')
conn.commit()

# Команда для добавления нового ключа
@dp.message_handler(commands=['addkey'])
async def add_key(message: types.Message):
    args = message.text.split()
    if len(args) != 2:
        await message.reply("Использование: /addkey КЛЮЧ")
        return

    key = args[1]
    try:
        cursor.execute("INSERT INTO licenses (key) VALUES (?)", (key,))
        conn.commit()
        await message.reply(f"Ключ {key} добавлен!")
    except:
        await message.reply("Этот ключ уже существует!")

# Проверка ключа через HTTP-запрос
@dp.message_handler()
async def check_license(message: types.Message):
    key = message.text.strip()
    cursor.execute("SELECT * FROM licenses WHERE key=? AND active=1", (key,))
    if cursor.fetchone():
        await message.reply("valid")  # Ключ верный
    else:
        await message.reply("invalid")  # Ключ неверный

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
