# 🚀 RAILWAY DEPLOYMENT - Copy These Exact Steps

**After your code is on GitHub, follow this exactly!**

---

## STEP-BY-STEP (5 MINUTES)

### 1. Go to Railway
```
https://railway.app
```

### 2. Click "Sign up" → Connect with GitHub
- Choose GitHub (easiest)
- GitHub will ask permission
- Click "Authorize"

### 3. Create New Project
- Click: "New Project"
- Select: "Deploy from GitHub"

### 4. Select Your Repository
- Click "Select Repo"
- Find: `telegram-music-bot`
- Click it

### 5. Railway Will Ask for Permission
- Click: "Install & Authorize"
- (GitHub will open)
- Click: "Install"
- It will redirect back

### 6. Railway Dashboard Opens
- You'll see your deployment starting
- Might say "Building..."
- That's normal

### 7. Click "Add Variables"
- Add EACH variable one by one
- Copy from `.env.example`

**Exactly copy these:**

```
BOT_TOKEN=8680937067:AAE885EaAnQ5S0Ik9BtJYgbgPEtJb0poJF4
API_ID=31656328
API_HASH=a9e57623a4408a41418ca647b2f08950
STRING_SESSION=BACcYO4AwpXvS8BX28sA0MRNi_IcoIZo9N2pOuCzaVPoD6bk0oeZnRXTqF3al_LPp8B8wqdQOKrgxJpesMPdU7ZqkK07X1OZsXrGIaxq3M2_alZCVOfgyTbN8KJ2-sJEw_mzYRqIEuXJ-Sf9FLGdDTtOjutnZdSn3XpQU04RxAnUcjIiwQKb2tEXrOnsCmhiGiGJEvQ2aovqCQAdpvrP3aPDJHcCx2RAxfbRkU-erf8cNwXT5QnhDxIV37Ou53P_kLzidswEv-R6OvqSUrBgtwOfOBmcXyvWVZQiE7e2D-puD4Rr_uxhqovDa-rRNcPQXGr6hmr186-ITEF130u53d2rd5rlUgAAAAF1LT2ZAA
MONGO_DB_URI=mongodb+srv://aditya0:aditya0@cluster0.9m8897t.mongodb.net/?appName=Cluster0
MONGO_DB_NAME=music_bot
OWNER_ID=8335505032
LOGGER_ID=-1003858465326
BOT_NAME=MUSIC BOT
SUPPORT_CHAT=https://t.me/song_assistant
OPENAI_API_KEY=
OPENAI_MODEL=gpt-3.5-turbo
DEFAULT_QUEUE_LIMIT=50
MAX_SONG_DURATION=3600
DEBUG=False
```

### 8. Save Variables
- Click: "Save"
- Railway will re-deploy automatically

### 9. Wait for Deployment
- Should take 2-3 minutes
- You'll see logs scrolling
- Look for: "Bot running"

### 10. Done! ✅
- Your bot is now LIVE
- 24/7 running
- Check logs for any errors

---

## 🎮 TEST YOUR BOT

1. Open Telegram
2. Find your bot
3. Send: `/start`
4. Expected: Bot responds ✓
5. Send: `/help`
6. Expected: All commands listed ✓
7. Send: `/play hello`
8. Expected: Music starts ✓

---

## ✅ IF EVERYTHING WORKS

Congratulations! Your bot is now:
- ✅ On GitHub (backed up)
- ✅ On Railway (running 24/7)
- ✅ Ready to use!

---

## ❌ IF SOMETHING GOES WRONG

**Check Railway Logs:**
1. Go to your Railway project
2. Click: "Logs" tab
3. Look for red errors
4. Screenshot it if needed

**Common Issues:**

**Problem**: `ModuleNotFoundError`
- Fix: Railway is still building, wait 2 more minutes

**Problem**: `Bot token invalid`
- Fix: Check BOT_TOKEN value in variables (copy exact)

**Problem**: `Cannot connect to MongoDB`
- Fix: Check MONGO_DB_URI value (copy exact)

**Problem**: `Authentication failed`
- Fix: Check API_ID and API_HASH (exact copy)

---

## 📞 HELP

- Logger Channel: -1003858465326
- Support Chat: https://t.me/song_assistant
- GitHub Issues (if you want community help)

---

**You're done!** 🎉

Your bot is live and working!

