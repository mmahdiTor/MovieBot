import sqlite3
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import time
from api_time import timee

# تنظیمات اولیه
api_id = 20339752
api_hash = "7eabc168d48bb06a54908edd7a39cf45"
bot_token = "7398977393:AAGcUMYYAUiO4P-uUAf-HMcItk82c8HnXsY"
ADMIN_ID = 829156312
CHANNEL_ID = -1001844063729

app = Client("uploader", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

def buton(message):
  global boten
  keyboard = InlineKeyboardMarkup(row_width=2)
  btn = InlineKeyboardButton("عضویت اجباری",url = "tg://resolve?domain=HACK_AMNIAT_TO",callback_data="join")
  btn1 = InlineKeyboardButton("عضویت اجباری",url = "tg://resolve?domain=Zeroo_Porn",callback_data="join")
  btn2 = InlineKeyboardButton("عضویت اجباری",url = "tg://resolve?domain=ZerooPorn0",callback_data="join")
  btn3 = InlineKeyboardButton("عضویت اجباری",url = "tg://resolve?domain=ILLUMinAtiiMTH",callback_data="join")
  btn4 = InlineKeyboardButton("عضو شدم",callback_data="check_join")
  keyboard.add(btn,btn1,btn2,btn3,btn4)
  boten = app.reply_to(message,"""
🔎 شما اول باید در کانال عضو بشید:

بعد از عضویت لطفا /start رو بفرستید
                """
              ,reply_markup=keyboard)
  
# دیتابیس‌ها
def init_db():
    with sqlite3.connect('db/Sql_member.db') as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS member(chat_id INTEGER PRIMARY KEY)")
    with sqlite3.connect("db/videos.db") as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id INTEGER,
            timestamp TEXT)""")

# مدیریت عضویت اجباری
async def is_subscribed(user_id):
    channels = ["@Zeroo_Porn1", "@HACK_AMNIAT_TO", "@ILLUMinAtiiMTH", "@ZerooPorn0"]
    for ch in channels:
        try:
            await app.get_chat_member(ch, user_id)
        except:
            return False
    return True

@app.on_message(filters.command('start'))
async def start_handler(client, message):
    user_id = message.from_user.id
    
    # ثبت کاربر
    with sqlite3.connect('db/Sql_member.db') as conn:
        conn.execute("INSERT OR IGNORE INTO member (chat_id) VALUES (?)", (user_id,))
    
    if user_id == ADMIN_ID:
        markup = ReplyKeyboardMarkup([['🎁 آپلود فیلم 🎁', '💎 ارسال پیام همگانی 💎'], ['⚠ تعداد اعضای ربات ⚠', '💡 راهنما 💡']], resize_keyboard=True)
        await message.reply("سلام ادمین عزیز، خوش اومدی!", reply_markup=markup)
        return

    if not await is_subscribed(user_id):
        buttons = [
            [InlineKeyboardButton('عضویت در کانال 1', url="tg://resolve?domain=HACK_AMNIAT_TO",callback_data="join")],
            [InlineKeyboardButton('عضویت در کانال 2', url="tg://resolve?domain=Zeroo_Porn",callback_data="join")],
            [InlineKeyboardButton('عضویت در کانال 3', url="tg://resolve?domain=ZerooPorn0",callback_data="join")],
            [InlineKeyboardButton('عضویت در کانال 4', url="tg://resolve?domain=ILLUMinAtiiMTH",callback_data="join")],
            [InlineKeyboardButton("عضو شدم", callback_data="check_join")]
        ]
        await message.reply("لطفا ابتدا در کانال‌های ما عضو شوید.", reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await message.reply("به ربات خوش آمدید!")

@app.on_callback_query(filters.regex("check_join"))
def check_join(call):
  call_chat_id = call.from_user.id
  bot.delete_message(call_chat_id,message_id=boten.id)
  chat_id ="@Zeroo_Porn"
  chat_id1 = "@HACK_AMNIAT_TO"
  chat_id2 = "@ILLUMinAtiiMTH"
  chat_id3 = "@ZerooPorn0"
  
  chanell = -1001844063729
  
  user_id = call.from_user.id
  user = app.get_chat_member(chat_id,user_id)
  user1 = app.get_chat_member(chat_id1,user_id)
  user2 = app.get_chat_member(chat_id2,user_id)
  user3 = app.get_chat_member(chat_id3,user_id)
  st = ['member','administrator','creator']
  if user.status in st and user1.status in st and user2.status in st and user3.status in st:
    try :
      id_code = id_code1.split()
      s = id_code[1]
      try :
        mes = bot.forward_message(call_chat_id, chanell, s)
        bot.send_message(call_chat_id,"ویدیو ظرف 20 ثانیه بعد حذف خواهد شد ❌ \n لطفا در سیو مسیج خود ذخیرش کنید ✅")
        time.sleep(20)
        bot.delete_message(call_chat_id,message_id=mes.id)
      except :
        bot.send_message(call_chat_id,"این فایل وجود ندارد")
    except :
      time_all = timee()
      time1 = time_all[0]
      time2 = time_all[1]
      firstname = call.from_user.first_name
      bot.send_message(call_chat_id,f"""
                      سلام خیلی خوش اومدی {firstname} به ربات ما 💥
                      امروز <b>{time1}</b> و ساعت <b>{time2}</b> هست 🌐
                      """,parse_mode="HTML")
  else :
    buton(call)
    bot.answer_callback_query(callback_query_id=call.id,text="شما هنوز عضو نشده اید")
  

# جایگزین Pyromod ask
@app.on_message(filters.regex("ارسال پیام همگانی") & filters.user(ADMIN_ID))
async def broadcast_start(client, message):
    await message.reply("لطفا پیامی که می‌خواهید برای همه ارسال شود را بفرستید (پاسخ دهید/Reply):")
    
    @app.on_message(filters.reply & filters.user(ADMIN_ID), group=1)
    async def get_broadcast_text(c, m):
        m.stop_propagation() # متوقف کردن هندلرهای دیگر
        with sqlite3.connect('db/Sql_member.db') as conn:
            users = conn.execute("SELECT chat_id FROM member").fetchall()
        
        sent = 0
        for user in users:
            try:
                await m.forward(user[0])
                sent += 1
                await asyncio.sleep(0.05) # جلوگیری از فلود شدن
            except: pass
        await m.reply(f"پیام با موفقیت برای {sent} نفر ارسال شد.")

init_db()
app.run()