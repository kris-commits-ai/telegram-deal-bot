
print("🚀 Запущен бот из файла:", __file__)
mport asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# === Настройки ===
BOT_TOKEN = "7617854158:AAHdN8KR74iguSk0o2uc8vcsbq6xsP_lT9M"  # Вставь сюда токен бота

# Карта форм по номеру встречи
FORMS = {
    "1": "https://docs.google.com/forms/d/e/1FAIpQLSf-HLgog5fei68ZmebxNrnW7iLDEwqYCgyASqNpbzDuirJ1HQ/viewform",
    "2": "https://docs.google.com/forms/d/e/FORM_ID_2/viewform",
    "3": "https://docs.google.com/forms/d/e/FORM_ID_3/viewform"
}

# ID полей Google Forms (узнаем через "Предварительно заполнить")
FIELDS = {
    "deal_id": "entry.1355511633",     # ID сделки
    "client_name": "entry.1094477986", # Название клиента
    "full_name": "entry.1237317028"    # Фамилия Имя
}

# === Логика ===
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Отправь данные в формате:\nID, Клиент, № встречи, Фамилия Имя")

@dp.message()
async def handle_message(message: types.Message):
    try:
        deal_id, client_name, meeting_number, full_name = [x.strip() for x in message.text.split(",")]
    except ValueError:
        await message.reply("❌ Формат: ID, Клиент, № встречи, Фамилия Имя")
        return

    base_form_url = FORMS.get(meeting_number)
    if not base_form_url:
        await message.reply("❌ Неверный номер встречи. Доступные: " + ", ".join(FORMS.keys()))
        return

    link = (
        f"{base_form_url}?usp=pp_url"
        f"&{FIELDS['deal_id']}={deal_id.replace(' ', '+')}"
        f"&{FIELDS['client_name']}={client_name.replace(' ', '+')}"
        f"&{FIELDS['full_name']}={full_name.replace(' ', '+')}"
    )

    await message.reply(f"✅ Ваша форма готова:\n{link}")

# === Запуск ===
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
