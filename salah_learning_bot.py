# Salah Learning Bot 🌙
# Learn daily prayer recitations step-by-step
# Includes: tracking, daily reminder, resume feature

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import time
import json, pytz, asyncio

TOKEN = ""
SGT = pytz.timezone("Asia/Singapore")

PROGRESS_FILE = "progress.json"
USERS_FILE = "users.json"


def load_json(filename):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except:
        return {}

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f)

def save_progress(user_id, day):
    progress = load_json(PROGRESS_FILE)
    progress[str(user_id)] = day
    save_json(PROGRESS_FILE, progress)

def get_progress(user_id):
    progress = load_json(PROGRESS_FILE)
    return progress.get(str(user_id), 1)

def register_user(user_id):
    users = load_json(USERS_FILE)
    users[str(user_id)] = True
    save_json(USERS_FILE, users)

def get_all_users():
    users = load_json(USERS_FILE)
    return list(users.keys())


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    register_user(user_id)
    save_progress(user_id, 1)

    await update.message.reply_text(
        "🌙 *Assalamu'alaikum!*

"
        "Welcome to your 7-Day Salah Learning Bot 🕋
"
        "Each day we’ll learn part of the solat step-by-step.

"
        "Type /day1 to begin, or /continue if you’ve started before.",
        parse_mode="Markdown"
    )


async def continue_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    register_user(user_id)
    day = get_progress(user_id)
    await update.message.reply_text(
        f"👋 You last stopped at *Day {day}*. Let's continue!",
        parse_mode="Markdown"
    )
    await globals()[f"day{day}"](update, context)


async def send(update, text):
    await update.message.reply_text(text, parse_mode="Markdown")


async def day1(update, context):
    user_id = update.message.from_user.id
    save_progress(user_id, 1)
    await send(update,
        "📖 *Day 1: Surah Al-Fātiḥah*

"
        "بِسْمِ اللَّهِ الرَّحْمَـٰنِ الرَّحِيمِ
"
        "_Bismillāhi r-raḥmāni r-raḥīm_
"
        "“In the name of Allah, the Most Kind, the Most Merciful.”

"
        "Continue till the end, memorize line-by-line 💭
"
        "This surah is recited in *every rak‘ah*.

"
        "Type /quiz1 to test yourself!"
    )

async def quiz1(update, context):
    user_id = update.message.from_user.id
    save_progress(user_id, 2)
    await send(update,
        "🧠 *Quiz 1*
What do we recite in every rak‘ah?

"
        "1️⃣ Al-Ikhlāṣ
2️⃣ *Al-Fātiḥah* ✅
3️⃣ Al-Falaq

"
        "Type /day2 to continue!"
    )

# (Other days and quizzes omitted here for brevity — full code same as previous message)

print("✅ Bot is running... Send /start in Telegram to begin.")
