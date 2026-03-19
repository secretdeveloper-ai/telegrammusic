# 🔐 Credentials Reference Card

## ✅ Credentials You Already Have

### Telegram Bot
```
BOT_TOKEN: 8680937067:AAE885EaAnQ5S0Ik9BtJYgbgPEtJb0poJF4
Purpose: Communication with Telegram Bot API
Added: ✅ YES
Where to use: .env as BOT_TOKEN
```

### Telegram API (Pyrogram)
```
API_ID: 31656328
Purpose: Telegram API access for Pyrogram client
Added: ✅ YES
Where to use: .env as API_ID

API_HASH: a9e57623a4408a41418ca647b2f08950
Purpose: Telegram API authentication
Added: ✅ YES
Where to use: .env as API_HASH
```

### Pyrogram String Session
```
STRING_SESSION: BACcYO4AwpXvS8BX28sA0MRNi_IcoIZo9N2pOu...
Purpose: User account authentication for music streaming
Added: ✅ YES
Where to use: .env as STRING_SESSION
Note: This is your personal Telegram account session
```

### MongoDB Database
```
MONGO_DB_URI: mongodb+srv://aditya0:aditya0@cluster0.9m8897t.mongodb.net/?appName=Cluster0
Purpose: Cloud database for storing group data, queues, user info
Added: ✅ YES (Pre-configured)
Where to use: .env as MONGO_DB_URI
Note: Already points to your Atlas cluster
```

### Owner & Support
```
OWNER_ID: Your Telegram ID (need to add)
Purpose: Identify bot owner for special permissions
Where to get: Your own Telegram user ID
Where to use: .env as OWNER_ID

LOGGER_ID: -1003858465326
Purpose: Channel to send bot logs and alerts
Added: ✅ YES
Where to use: .env as LOGGER_ID
Type: Private channel ID (negative number)

SUPPORT_CHAT: https://t.me/song_assistant
Purpose: Support chat link shown to users
Added: ✅ YES
Where to use: .env as SUPPORT_CHAT
```

### Bot Configuration
```
BOT_NAME: MUSIC BOT
Purpose: Name displayed in help/about commands
Added: ✅ YES
Where to use: .env as BOT_NAME
Customizable: YES
```

## ⚠️ Credentials You STILL NEED

### 1️⃣ OpenAI API Key (CRITICAL)
```
Variable: OPENAI_API_KEY
Example: sk-proj-XxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXx
Purpose: ChatGPT/GPT-4 AI integration
Where to get: https://platform.openai.com/api-keys
Steps:
  1. Create OpenAI account
  2. Go to API Keys section
  3. Click "Create new secret key"
  4. Copy entire key
  5. Add to .env as: OPENAI_API_KEY=sk-...

Cost: $5-20/month for moderate usage
Recommended plan: Pay-as-you-go
Free trial: $5 initial credit
```

### 2️⃣ Spotify Credentials (OPTIONAL but RECOMMENDED)
```
SPOTIFY_CLIENT_ID: (get from Spotify Developer Dashboard)
SPOTIFY_CLIENT_SECRET: (get from Spotify Developer Dashboard)
Purpose: Search and play music from Spotify
Steps:
  1. Go to https://developer.spotify.com/dashboard
  2. Create an app
  3. Accept terms
  4. Copy Client ID and Client Secret
  5. Add to .env

Cost: FREE (no payment needed)
Benefits: Better music search results
Can be skipped: YES (uses YouTube as fallback)
```

### 3️⃣ YouTube API Key (OPTIONAL)
```
YOUTUBE_API_KEY: (get from Google Cloud Console)
Purpose: Improved YouTube search and metadata
Steps:
  1. Go to https://console.cloud.google.com
  2. Create new project
  3. Enable YouTube Data API v3
  4. Create API key
  5. Add to .env

Cost: FREE (10,000 requests/day limit)
Can be skipped: YES (bot works without it)
```

## 📋 .env File Template

Save this as `.env` and fill in the missing parts:

```bash
# TELEGRAM BOT (✅ Complete)
BOT_TOKEN=8680937067:AAE885EaAnQ5S0Ik9BtJYgbgPEtJb0poJF4
OWNER_ID=YOUR_TELEGRAM_ID_HERE
LOGGER_ID=-1003858465326
BOT_NAME=MUSIC BOT
SUPPORT_CHAT=https://t.me/song_assistant

# PYROGRAM (✅ Complete)
API_ID=31656328
API_HASH=a9e57623a4408a41418ca647b2f08950
STRING_SESSION=BACcYO4AwpXvS8BX28sA0MRNi_IcoIZo9N2pOuCzaVPoD6bk0oeZnRXTqF3al_LPp8B8wqdQOKrgxJpesMPdU7ZqkK07X1OZsXrGIaxq3M2_alZCVOfgyTbN8KJ2-sJEw_mzYRqIEuXJ-Sf9FLGdDTtOjutnZdSn3XpQU04RxAnUcjIiwQKb2tEXrOnsCmhiGiGJEvQ2aovqCQAdpvrP3aPDJHcCx2RAxfbRkU-erf8cNwXT5QnhDxIV37Ou53P_kLzidswEv-R6OvqSUrBgtwOfOBmcXyvWVZQiE7e2D-puD4Rr_uxhqovDa-rRNcPQXGr6hmr186-ITEF130u53d2rd5rlUgAAAAF1LT2ZAA

# MONGODB (✅ Complete)
MONGO_DB_URI=mongodb+srv://aditya0:aditya0@cluster0.9m8897t.mongodb.net/?appName=Cluster0
MONGO_DB_NAME=music_bot

# OPENAI - 🔴 YOU NEED THIS
OPENAI_API_KEY=sk-your-openai-key-here
OPENAI_MODEL=gpt-3.5-turbo

# SPOTIFY (Optional)
SPOTIFY_CLIENT_ID=
SPOTIFY_CLIENT_SECRET=

# YOUTUBE (Optional)
YOUTUBE_API_KEY=

# BOT SETTINGS
DEFAULT_QUEUE_LIMIT=50
MAX_SONG_DURATION=3600

# WEBHOOK (For Railway)
TELEGRAM_WEBHOOK_URL=https://your-app-name.railway.app
WEBHOOK_PORT=8080

# DEBUG
DEBUG=False
```

## 🎯 Priority List

### Must Have (To Run Bot)
1. ✅ BOT_TOKEN - Already provided
2. ✅ API_ID - Already provided
3. ✅ API_HASH - Already provided
4. ✅ STRING_SESSION - Already provided
5. ✅ MONGO_DB_URI - Already provided
6. 🔴 OPENAI_API_KEY - GET THIS NOW!

### Should Have (Better Experience)
7. SPOTIFY_CLIENT_ID & SECRET
8. YOUTUBE_API_KEY
9. OWNER_ID (your Telegram ID)

### Optional
10. Everything else has defaults

## 🔓 How to Get Your Telegram ID

### Method 1: Using @userinfobot
1. Open Telegram
2. Search `@userinfobot`
3. Start chat with bot
4. It shows your user ID
5. Copy and add to .env as OWNER_ID

### Method 2: From Bot Messages
1. `/start` the bot in a group
2. Check logs or bot responses
3. Your ID will be shown

## 🚨 SECURITY WARNING

### NEVER Share:
- ❌ BOT_TOKEN
- ❌ API_HASH
- ❌ STRING_SESSION
- ❌ OPENAI_API_KEY
- ❌ MONGO_DB_URI
- ❌ Any .env file

### How to Protect:
✅ Use GitHub `.gitignore` (ignore .env)
✅ Use Railway secrets (never paste in code)
✅ Regenerate if exposed
✅ Use environment variables only
✅ Never commit .env to repo

## 📊 Credentials Checklist

```
Setup Checklist:
[ ] BOT_TOKEN verified - ✅
[ ] API_ID verified - ✅
[ ] API_HASH verified - ✅
[ ] STRING_SESSION valid - ✅
[ ] MONGO_DB_URI working - ✅
[ ] OPENAI_API_KEY obtained - ❌ DO THIS
[ ] Test .env file with bot
[ ] Deploy to Railway
[ ] Monitor logs
[ ] Add to support chat
```

## 🆘 Verification

To verify all credentials are correct:

```bash
# Test OpenAI
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# Test Telegram Bot
curl https://api.telegram.org/bot$BOT_TOKEN/getMe

# Test MongoDB
mongosh "$MONGO_DB_URI"
```

## 📞 Need Help?

- OpenAI Docs: https://platform.openai.com/docs
- Telegram API: https://core.telegram.org/bots
- MongoDB Atlas: https://www.mongodb.com/cloud/atlas
- Support Chat: https://t.me/song_assistant

---

**Next Action: Get OpenAI API key and add to .env** 🚀
