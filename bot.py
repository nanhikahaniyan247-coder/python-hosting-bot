import telebot, os
from process_manager import start_process, stop_process, is_running
from keep_alive import keep_alive

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = 7381777230

bot = telebot.TeleBot(BOT_TOKEN)
UPLOAD = "uploads"
os.makedirs(UPLOAD, exist_ok=True)

def owner(m): 
    return m.from_user.id == OWNER_ID

@bot.message_handler(commands=["start"])
def start(m):
    if not owner(m): return
    bot.reply_to(m,
    "🤖 Python Hosting Bot\n"
    "/files\n/startfile name.py\n/stopfile name.py\n"
    "/delete name.py\n/status name.py\n\n"
    "📤 Send .py file")

@bot.message_handler(content_types=["document"])
def upload(m):
    if not owner(m): return
    if not m.document.file_name.endswith(".py"):
        bot.reply_to(m,"Only .py allowed"); return
    f = bot.get_file(m.document.file_id)
    d = bot.download_file(f.file_path)
    open(f"{UPLOAD}/{m.document.file_name}","wb").write(d)
    bot.reply_to(m,"✅ Uploaded")

@bot.message_handler(commands=["files"])
def files(m):
    if owner(m):
        bot.reply_to(m,"\n".join(os.listdir(UPLOAD)) or "Empty")

@bot.message_handler(commands=["startfile"])
def sf(m):
    if owner(m):
        name=m.text.split()[1]
        start_process(f"{UPLOAD}/{name}")
        bot.reply_to(m,"▶️ Started")

@bot.message_handler(commands=["stopfile"])
def sp(m):
    if owner(m):
        name=m.text.split()[1]
        stop_process(f"{UPLOAD}/{name}")
        bot.reply_to(m,"⏹ Stopped")

@bot.message_handler(commands=["delete"])
def dl(m):
    if owner(m):
        name=m.text.split()[1]
        stop_process(f"{UPLOAD}/{name}")
        os.remove(f"{UPLOAD}/{name}")
        bot.reply_to(m,"🗑 Deleted")

@bot.message_handler(commands=["status"])
def st(m):
    if owner(m):
        name=m.text.split()[1]
        s=is_running(f"{UPLOAD}/{name}")
        bot.reply_to(m,"RUNNING" if s else "STOPPED")

keep_alive()
bot.infinity_polling()
