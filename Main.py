import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from PIL import Image
import io

# حط التوكن تبعك هون
BOT_TOKEN = os.getenv("BOT_TOKEN", "ضع_التوكن_هنا")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 اهلا! انا بوت تحليل الشارتات\n\n"
        "📊 ابعتلي صورة الشارت وانا بحللها ICT + Gemini style\n\n"
        "ارسل الصورة الان 👇"
    )

async def analyze_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ جاري تحليل الشارت... ثواني")
    
    try:
        photo_file = await update.message.photo[-1].get_file()
        photo_bytes = await photo_file.download_as_bytearray()
        
        image = Image.open(io.BytesIO(photo_bytes))
        w, h = image.size

        # تحليل مبدئي - هون بنقدر نربط Gemini API لاحقا
        analysis = f"""
📊 **تحليل الشارت - ICT Concept**

✅ **تم استلام الصورة:** {w}x{h}

🔍 **التحليل الأولي:**

1️⃣ **الهيكل (Structure):**
- شوف الـ BOS و CHOCH
- حدد اذا السوق Bullish ولا Bearish

2️⃣ **السيولة (Liquidity):**
- دور على Buy Side و Sell Side
- Equal Highs / Equal Lows

3️⃣ **المناطق المهمة:**
- Order Block
- Fair Value Gap (FVG)
- Breaker Block

4️⃣ **الدخول المقترح:**
- استنى تأكيد على الـ 5m / 1m
- دخول مع اعادة اختبار OB + FVG

⚠️ **ملاحظة:** هاد تحليل آلي مبدئي. 
للتحليل المتقدم بـ Gemini، رح نربط API قريبا.

ابعت شارت ثاني اذا بدك 👇
        """
        
        await update.message.reply_text(analysis, parse_mode='Markdown')
        
    except Exception as e:
        logging.error(e)
        await update.message.reply_text(f"صار خطأ: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, analyze_photo))
    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
