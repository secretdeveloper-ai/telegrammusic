# 🚀 START HERE

**Your bot is ready. Follow these 3 simple steps.**

---

## 📱 Step 1: Get Your Telegram ID (2 minutes)

1. Open Telegram
2. Search for bot: `@userinfobot`
3. Send: `/start`
4. Copy the number that shows (e.g., `123456789`)
5. **Save it somewhere** ← You need this!

---

## 💻 Step 2: Upload to GitHub (5 minutes)

### If you have GitHub already:
1. Go to https://github.com/new
2. Create repo named: `telegram-music-bot`
3. Follow [GITHUB_UPLOAD_GUIDE.md](GITHUB_UPLOAD_GUIDE.md)

### If you DON'T have GitHub:
1. Go to https://github.com/signup
2. Create account
3. Then follow [GITHUB_UPLOAD_GUIDE.md](GITHUB_UPLOAD_GUIDE.md)

---

## 🚁 Step 3: Deploy on Railway (3 minutes)

1. Go to https://railway.app
2. Click "Sign up with GitHub"
3. Connect your GitHub account
4. Click "New Project"
5. Select "Deploy from GitHub"
6. Pick your `telegram-music-bot` repo
7. **Add these variables:**

```
BOT_TOKEN=8680937067:AAE885EaAnQ5S0Ik9BtJYgbgPEtJb0poJF4
API_ID=31656328
API_HASH=a9e57623a4408a41418ca647b2f08950
STRING_SESSION=BACcYO4AwpXvS8BX28sA0MRNi_IcoIZo9N2pOuCzaVPoD6bk0oeZnRXTqF3al_LPp8B8wqdQOKrgxJpesMPdU7ZqkK07X1OZsXrGIaxq3M2_alZCVOfgyTbN8KJ2-sJEw_mzYRqIEuXJ-Sf9FLGdDTtOjutnZdSn3XpQU04RxAnUcjIiwQKb2tEXrOnsCmhiGiGJEvQ2aovqCQAdpvrP3aPDJHcCx2RAxfbRkU-erf8cNwXT5QnhDxIV37Ou53P_kLzidswEv-R6OvqSUrBgtwOfOBmcXyvWVZQiE7e2D-puD4Rr_uxhqovDa-rRNcPQXGr6hmr186-ITEF130u53d2rd5rlUgAAAAF1LT2ZAA
MONGO_DB_URI=mongodb+srv://aditya0:aditya0@cluster0.9m8897t.mongodb.net/?appName=Cluster0
MONGO_DB_NAME=music_bot
OWNER_ID=YOUR_TELEGRAM_ID_HERE
LOGGER_ID=-1003858465326
BOT_NAME=MUSIC BOT
SUPPORT_CHAT=https://t.me/song_assistant
OPENAI_API_KEY=
OPENAI_MODEL=gpt-3.5-turbo
DEFAULT_QUEUE_LIMIT=50
MAX_SONG_DURATION=3600
DEBUG=False
```

8. **IMPORTANT**: Replace `YOUR_TELEGRAM_ID_HERE` with the number from Step 1
9. Click "Deploy"
10. Wait 2-3 minutes...
11. **Done!** ✅ Your bot is live!

---

## 🎮 Test Your Bot

1. Open Telegram
2. Find your bot (bot username from BotFather)
3. Create or go to a group
4. Add your bot to the group
5. Try: `/start`
6. Try: `/help`
7. Try: `/play hello`

If the bot responds → **It works!** 🎉

---

## 💡 That's It!

Your bot is now:
- ✅ Running 24/7 on Railway ☁️
- ✅ Backed up on GitHub 💾
- ✅ Ready to play music 🎵

---

## 📚 Need More Help?

[View Full Docs](READY_TO_DEPLOY.md)

---

## 🎵 Available Commands

**Music**
```
/play <song>          Play a song
/queue                Show queue
/skip                 Next song
/shuffle              Random order
```

**Groups** (Admin)
```
/init                 Setup group
/admin_add <id>       Make admin
/ban <id>             Block user
```

**Owner** (Your ID only)
```
/broadcast <message>  Send to all groups
```

**Other**
```
/help                 All commands
/ask <question>       Ask AI (if key added)
/stats                Group statistics
```

---

## ⚠️ Important

- Keep your OWNER_ID secret (don't share it)
- MongoDB is already configured ✅
- YouTube works automatically ✅
- OPENAI_API_KEY is optional (leave empty if not needed)

---

**Questions?** Check your bot's logger channel: -1003858465326

---

**Happy music! 🎵**

