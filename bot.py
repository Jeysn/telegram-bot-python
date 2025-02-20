import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
import asyncio
import requests
import os
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

NEWS_API_KEY = "9c1b2347ca9944dd9d9f85b57949164b"  # API kalitingizni kiriting
query = "миграция OR рейд OR патент OR регистрация"  # Rus tilida so‘zlar
url = f"https://newsapi.org/v2/everything?q={query}&language=ru&sortBy=publishedAt&apiKey={NEWS_API_KEY}"

response = requests.get(url).json()
 # API dan kelgan javobni tekshirish



# ⚙️ API kalitlar
TOKEN = "7925206129:AAHbfysy2hkm2LCesm96gayam_XnI8diR2I"
OPENWEATHER_API_KEY = "3ce69eb0c4cb318cdf05038e2fc4500b"
NEWS_API_KEY = "9c1b2347ca9944dd9d9f85b57949164b"

# 🔹 Bot va dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()

# 🔹 Log sozlamalari
logging.basicConfig(level=logging.INFO)

# ✅ /start – Bot haqida ma’lumot
@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("👋 Assalomu alaykum, hurmatli O'zbekistondan kelgan do'stlar Sizga quyidagi xizmatlarni taqdim etaman, ayniqsa, Rusiyada bo'lib turgan o'zbeklar uchun \n"
                         "1   "
                         "🌦 Ob-havo ma'lumotlari Rusiya shaharlarining ob-havo holatini bilish uchun: /OB_HAVO [shahar]\n"
                         "2  "
                         "📰 Yangiliklar Rusiya va O'zbekistondagi eng so'nggi yangiliklarni bilish uchun:       /XABARLAR\n"
                         "3  "
                         "📢 Migratsiya va hukumat yangiliklari Rusiya hududidagi patent va migratsiya yangiliklari bilan tanishish uchun: /HUKUMAT\n"
                         "4  "
                         "🔄 Matn tarjimasi — O'zbek tilidan Rus tiliga yoki aksincha tez va oson tarjima qilish uchun:  /TARJIMA ")


# ✅ /xabarlar – Yangiliklarni olish
@dp.message(Command("XABARLAR"))
async def news_command(message: Message):
    query = "миграция OR рейд OR патент OR регистрация"  # Rus tilida so‘zlar
    url = f"https://newsapi.org/v2/everything?q={query}&language=ru&sortBy=publishedAt&apiKey={NEWS_API_KEY}"   
    response = requests.get(url).json()
    articles = response.get("articles", [])

    if not articles:
        await message.answer("❌ Yangiliklar topilmadi!")
        return

    news_text = "\n\n".join([f"📰 {article['title']}\n🔗 {article['url']}" for article in articles[:5]])
    await message.answer("📢 Eng so‘nggi yangiliklar:\n\n" + news_text)

response = requests.get(url).json()
print(response)  # API dan kelgan javobni tekshirish
@dp.message(Command("news"))
async def news_command(message: Message):
    print("📡 /news buyrug‘i qabul qilindi!")  # Terminal uchun
    try:
        await message.answer("📢 Yangiliklarni olishga harakat qilmoqdaman...")
        print("✅ Xabar foydalanuvchiga yuborildi!")  # Terminal uchun
    except Exception as e:
        print(f"❌ Xabar yuborishda xatolik: {e}")  # Xatolikni ko‘rsatish

# ✅ /hukumat – Migratsiya va reydlar yangiliklari
@dp.message(Command("HUKUMAT"))
async def gov_news_command(message: Message):
    url = "https://xn--b1aew.xn--p1ai/news/rss"  # Rossiya IIV rasmiy yangiliklar RSS
    response = requests.get(url)

    if response.status_code != 200:
        await message.answer("❌ Hukumat yangiliklarini olishda xatolik yuz berdi.")
        return

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(response.text, "xml")
    items = soup.find_all("item")[:5]

    if not items:
        await message.answer("📭 Hozircha migratsiya va reydlar haqida yangilik yo‘q.")
        return

    news_text = "\n\n".join([f"📰 {item.title.text}\n🔗 {item.link.text}" for item in items])
    await message.answer("🚨 Migratsiya va reydlar bo‘yicha yangiliklar:\n\n" + news_text)

# ✅ /tarjima – Matn tarjima qilish
@dp.message(Command("TARJIMA"))
async def translate_command(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("❗️ Iltimos, tarjima qilish uchun matn kiriting: /tarjima [matn]")
        return

    text = args[1]
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=uz&dt=t&q={text}"
    response = requests.get(url).json()

    translated_text = response[0][0][0] if response else "❌ Tarjima amalga oshmadi!"
    await message.answer(f"🔄 Tarjima:\n\n{text} ➡️ {translated_text}")



# ✅ /weather buyrug‘i - Ob-havo ma’lumotlarini olish (GPS orqali)






# ✅ Foydalanuvchi joylashuv yuborganda ob-havo olish

@dp.message(Command("weather"))
async def weather_command(message: Message):
    await message.answer("🌍 Iltimos, ob-havo ma’lumotlari uchun joylashuvingizni yuboring.", reply_markup=location_button)
@dp.message()
async def get_weather_by_location(message: Message):
      if message.location:
          lat = message.location.latitude
          lon = message.location.longitude
          print(f"📍 Joylashuv qabul qilindi: {lat}, {lon}")

          url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric&lang=uz"
          response = requests.get(url).json()

          if response.get("cod") == 200:
              weather_info = (
                  f"🌆 Shahar: {response['name']}\n"
                  f"🌡 Harorat: {response['main']['temp']}°C\n"
                  f"🌬 Shamol tezligi: {response['wind']['speed']} m/s\n"
                 f"⛅️ Holati: {response['weather'][0]['description'].capitalize()}"
              )
              await message.answer(weather_info)
          else:
              await message.answer("❌ Ob-havo ma’lumotlarini olishda xatolik yuz berdi.")
      else:
          await message.answer("❗️ Iltimos, GPS joylashuvingizni yuboring.")

# ✅ Botni ishga tushirish
if __name__ == "__main__":
    async def main():
        logging.info("🤖 Bot ishga tushdi!")
        await dp.start_polling(bot)

    asyncio.run(main())
