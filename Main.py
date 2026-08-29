import telebot
import google.generativeai as genai
import io
import os
from PIL import Image

TOKEN = os.environ.get("BOT_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_KEY")

genai.configure(api_key=GEMINI_KEY)
bot = telebot.TeleBot(TOKEN)

PROMPT = """انت محلل ICT/SMC محترف. حلل الصورة المرفقة بدقة.
1. اقرأ كل البيانات: الزوج, الفريم, السعر, RSI, MACD, المتوسطات, النقاط المحورية.
2. حلل ICT/SMC: CHoCH, BoS, FVG, Order Block, Liquidity Pools.
3. اعطي صفقة مقترحة كاملة: الاتجاه, الدخول, هدف1, هدف2, وقف خسارة.
الرد بالعربي: 📊 تحليل ICT/SMC كامل | [الزوج] - فريم [الفريم] ... ⚠️ ليس نصيحة مالية
"""

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "ارسل صورة الشارت وسأرجعلك تحليل ICT كامل + صفقة مقترحة 🔥")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    msg = bot.send_message(message.chat.id, "بقرأ الصورة وبحلل ICT/SMC...⏳")
    file_info = bot.get_file(message.photo[-1].file_id)
    img = bot.download_file(file_info.file_path)
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content([PROMPT, Image.open(io.BytesIO(img))])
    bot.edit_message_text(response.text, message.chat.id, msg.message_id)

print("البوت شغال...")
bot.polling()
