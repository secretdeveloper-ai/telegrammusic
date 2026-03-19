# 🎵 Quick Start - 5 Minutes to Running Bot

**Time to live bot: ~5 minutes** ⏱️

## 🎯 What You Have Now

Your bot is **already 95% configured**:
- ✅ Telegram bot credentials
- ✅ Pyrogram string session  
- ✅ MongoDB database
- ✅ All code ready
- ❌ OpenAI API key (need 1 minute)

## 🚀 Step 1: Get OpenAI API Key (1 min)

1. Go to: https://platform.openai.com/api-keys
2. Click "**Create new secret key**"
3. Copy the key (starts with `sk-`)
4. Save it somewhere safe

## 📝 Step 2: Create .env File (1 min)

### Windows:
```bash
cd C:\Users\adity\Downloads\telegram-music-bot
copy .env.example .env
notepad .env
```

### Mac/Linux:
```bash
cd ~/Downloads/telegram-music-bot
cp .env.example .env
nano .env
```

## ✏️ Step 3: Edit .env (1 min)

Find and update this line:

```env
OPENAI_API_KEY=sk-your-openai-key-here
```

Replace with your actual key:

```env
OPENAI_API_KEY=sk-proj-XxXxXxXxXxXxXxXxXxXxXxXxXxXxXx
```

Also add your Telegram ID:

```env
OWNER_ID=123456789  # Your Telegram ID
```

Save and close.

## 💾 Step 4: Install Dependencies (1 min)

### Windows:
```bash
cd C:\Users\adity\Downloads\telegram-music-bot
setup.bat
```

### Mac/Linux:
```bash
cd ~/Downloads/telegram-music-bot
chmod +x setup.sh
./setup.sh
source venv/bin/activate
```

## ▶️ Step 5: Run Bot (1 min)

```bash
python main.py
```

You should see:
```
🎵 Starting MUSIC BOT...
✅ Connected to MongoDB
✅ Pyrogram assistant account ready
✅ Bot initialization complete!
🔄 Starting with polling...
```

## 🎮 Test in Telegram

1. Open Telegram
2. Search for your bot (from username in BotFather)
3. Click "Start"
4. Try:
   ```
   /help
   /play hello world
   /queue
   /ask recommend songs
   ```

If it works → **Success!** 🎉

## ☁️ Deploy to Railway (3 min)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "ChatGPT bot with MongoDB"
   git push
   ```

2. **Connect to Railway**
   - Go to https://railway.app
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repo

3. **Add Variables**
   - Click Variables tab
   - Copy all variables from your `.env` file
   - Paste into Railway

4. **Deploy**
   - Click Deploy button
   - Wait 2-3 minutes
   - Done! ✅

## 🆘 Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt --upgrade
python main.py
```

### "MongoDB connection failed"
- Check MONGO_DB_URI in .env
- Verify internet connection
- Make sure IP is whitelisted in MongoDB Atlas

###  "Invalid API key"
- Verify OPENAI_API_KEY in .env
- No extra spaces
- Copy full key (including `sk-`)

### "Bot not responding in Telegram"
- Check BOT_TOKEN is correct
- Restart bot: Ctrl+C, then run again
- Check logs for errors

## 📋 Files Modified

These files were updated for ChatGPT + MongoDB:

```
✅ requirements.txt - Added OpenAI, MongoDB, Pyrogram
✅ config.py - New variables
✅ main.py - MongoDB + Pyrogram initialization
✅ handlers/*.py - Updated for async MongoDB
✅ utils/ - New MongoDB & GPT modules
✅ .env.example - Your credentials pre-filled
```

Old files (no longer used):
```
❌ utils/claude_assistant.py - Replaced with GPTAssistant
❌ utils/group_manager.py - Replaced with mongo version
❌ utils/queue_manager.py - Replaced with mongo version
❌ groups_data.json - No longer needed
❌ queues_data.json - No longer needed
```

## ✨ Key Features

Your bot now has:

🧠 **ChatGPT AI**
- Smart music recommendations
- Natural language processing
- `/ask` command

💾 **MongoDB Backend**
- Cloud database
- Always available
- Auto backups

🎤 **Pyrogram Streaming**
- Assistant account
- Better privacy
- Direct streaming

🔒 **Private Bot**
- Your credentials only
- No sharing needed
- Secure deployment

## 📱 Commands Quick Reference

**Music:**
```
/play song_name          Play a song
/queue                   Show queue
/skip                    Skip song
/next                    Next song info
/shuffle                 Shuffle queue
/clear_queue             Clear all songs
/remove 1                Remove song at position
```

**Admin:**
```
/init                    Init group
/info                    Group settings
/admin_add 12345         Add admin
/ban 12345               Ban user
/set_prefix !            Change prefix
/queue_limit 50          Set limit
```

**Other:**
```
/start                   Start bot
/help                    Show commands
/ask question            Ask AI
/stats                   Statistics
/about                   About bot
```

## 🎯 Next Steps

After running locally:

1. **Test all commands** - `/help` and `/play test`
2. **Add to group** - Invite bot to test group
3. **Test group features** - `/info`, `/admin_add`
4. **Monitor logs** - Check for errors
5. **Deploy to Railway** - Make it live

## ⚠️ Important

- **Keep .env private** - Don't share it
- **Regenerate credentials if exposed** - Security first
- **Update code regularly** - Check for updates
- **Monitor API usage** - OpenAI charges per request
- **Check database size** - MongoDB free tier: 512MB

## 🔗 Resources

- Bot docs: See README.md
- Setup guide: See CHATGPT_SETUP.md
- Conversion details: See CONVERSION_GUIDE.md
- Credentials: See CREDENTIALS_REFERENCE.md

## ⏱️ Estimated Time

```
Get API key:           ~1 min ⏱️
Edit .env file:         ~1 min ⏱️
Install dependencies:   ~1 min ⏱️
Run bot:               ~1 min ⏱️
Test commands:          ~1 min ⏱️
─────────────────────────────
Total:                 ~5 min ⏱️
```

## 🎉 You're Ready!

Everything is set up. Your bot is ready to:
- ✅ Play music from YouTube & Spotify
- ✅ Use ChatGPT for smart recommendations
- ✅ Store data in MongoDB (not local files)
- ✅ Stream via Pyrogram assistant
- ✅ Run on Railway for free

**Let's go!** 🚀

---

**Questions?** Check the support chat: https://t.me/song_assistant
