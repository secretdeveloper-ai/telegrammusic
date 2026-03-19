# ✅ Setup Checklist

## 📋 Pre-Setup Verification

- [ ] Read `QUICK_START.md` or `DOCUMENTATION_INDEX.md`
- [ ] Understand your pre-configured credentials
- [ ] Have Python 3.8+ installed
- [ ] Have text editor (Notepad, VS Code, etc.)
- [ ] Internet connection working
- [ ] GitHub account ready (for Railway)

---

## 🔑 Credentials Setup (5 minutes)

### ✅ Already Have (Pre-configured)
- [x] BOT_TOKEN - 8680937067:AAE885EaAnQ5S0Ik9BtJYgbgPEtJb0poJF4
- [x] API_ID - 31656328
- [x] API_HASH - a9e57623a4408a41418ca647b2f08950
- [x] STRING_SESSION - BACcYO4Aw... (Pyrogram session)
- [x] MONGO_DB_URI - mongodb+srv://aditya0:aditya0@...
- [x] LOGGER_ID - -1003858465326
- [x] SUPPORT_CHAT - https://t.me/song_assistant
- [x] BOT_NAME - MUSIC BOT

### ❌ Still Need to Get (1 minute each)
- [ ] **OPENAI_API_KEY**
  - Go to: https://platform.openai.com/api-keys
  - Click "Create new secret key"
  - Copy key (starts with `sk-`)
  - Save for next step
  
- [ ] **OWNER_ID** (optional but recommended)
  - Open Telegram
  - Search @userinfobot
  - Get your user ID number

- [ ] **SPOTIFY_CLIENT_ID & SECRET** (optional)
  - Go to: https://developer.spotify.com/dashboard
  - Create app
  - Copy credentials

- [ ] **YOUTUBE_API_KEY** (optional)
  - Go to: https://console.cloud.google.com
  - Create new project
  - Enable YouTube Data API
  - Create API key

---

## 📝 .env File Setup (2 minutes)

### Step 1: Create .env File

**Windows:**
```bash
cd C:\Users\adity\Downloads\telegram-music-bot
copy .env.example .env
```

**Mac/Linux:**
```bash
cd ~/Downloads/telegram-music-bot
cp .env.example .env
```

- [ ] .env file created

### Step 2: Open and Edit

**Windows:**
```bash
notepad .env
```

**Mac:**
```bash
nano .env
```

**Linux:**
```bash
vim .env
```

- [ ] .env file opened in editor

### Step 3: Update Required Variables

Find and update these lines:

```env
OPENAI_API_KEY=sk-your-key-here
OWNER_ID=your-telegram-id-here
```

Should become:

```env
OPENAI_API_KEY=sk-proj-XxXxXxXxXxXxXxXxXxXx  # Your OpenAI key
OWNER_ID=123456789  # Your Telegram ID
```

- [ ] OPENAI_API_KEY added
- [ ] OWNER_ID added  
- [ ] File saved

### Step 4: Verify Other Variables (should be pre-filled)

Check these are present:
- [ ] BOT_TOKEN=8680937067:...
- [ ] API_ID=31656328
- [ ] API_HASH=a9e57623a...
- [ ] STRING_SESSION=BACcYO4Aw...
- [ ] MONGO_DB_URI=mongodb+srv://aditya0:aditya0@...
- [ ] LOGGER_ID=-1003858465326
- [ ] SUPPORT_CHAT=https://t.me/song_assistant

All good? → Continue

---

## 💾 Install Dependencies (2 minutes)

### Option 1: Automatic Setup Script

**Windows:**
```bash
cd C:\Users\adity\Downloads\telegram-music-bot
setup.bat
```

- [ ] Completed without errors
- [ ] All packages installed

**Mac/Linux:**
```bash
cd ~/Downloads/telegram-music-bot
chmod +x setup.sh
./setup.sh
```

- [ ] Completed without errors
- [ ] All packages installed

### Option 2: Manual Setup

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

- [ ] Virtual environment created
- [ ] Environment activated
- [ ] Packages installed

---

## 🚀 Run Bot Locally (1 minute)

### Start the Bot

```bash
python main.py
```

### Expected Output

You should see:
```
🎵 Starting MUSIC BOT...
✅ Connected to MongoDB
✅ Pyrogram assistant account ready for music streaming
✅ Bot initialization complete!
🔄 Starting with polling...
```

- [ ] Bot started successfully
- [ ] MongoDB connected (✅)
- [ ] Pyrogram client connected (✅)
- [ ] No error messages
- [ ] Waiting for messages (shown in console)

### Common Issues

If you see errors:
- [ ] Check .env file for typos
- [ ] Verify OpenAI API key is valid
- [ ] Check internet connection
- [ ] Re-read error message carefully
- [ ] See TROUBLESHOOTING section below

---

## 🎮 Test in Telegram (2 minutes)

### Add Bot to Telegram

1. Open Telegram
2. Search for your bot (username from @BotFather)
3. Click "Start"

- [ ] Bot found in Telegram
- [ ] Chat with bot started

### Run Test Commands

**Test 1: Basic Help**
```
/help
```
- [ ] Shows command list
- [ ] No errors

**Test 2: Play Song**
```
/play test
```
- [ ] Returns song found
- [ ] Added to queue
- [ ] Shows ChatGPT info

**Test 3: Show Queue**
```
/queue
```
- [ ] Shows queued songs
- [ ] Shows position and duration

**Test 4: Ask AI**
```
/ask hello
```
- [ ] ChatGPT responds
- [ ] Natural conversation

**Test 5: Group Info**
```
/info
```
- [ ] Shows group settings
- [ ] Shows admin count
- [ ] Shows statistics

All tests passed? → Ready to deploy! ✅

---

## ☁️ Deploy to Railway (5 minutes)

### Step 1: Push to GitHub

```bash
git add .
git commit -m "Telegram Music Bot with ChatGPT"
git push origin main
```

- [ ] Code pushed to GitHub
- [ ] No merge conflicts

### Step 2: Connect Railway

1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Authorize GitHub
5. Select your repository

- [ ] Railway project created
- [ ] GitHub connected
- [ ] Repo selected

### Step 3: Add Environment Variables

In Railway dashboard → Variables:

Add all variables from your `.env` file:
- [ ] BOT_TOKEN
- [ ] OPENAI_API_KEY
- [ ] API_ID
- [ ] API_HASH
- [ ] STRING_SESSION
- [ ] MONGO_DB_URI
- [ ] OWNER_ID
- [ ] LOGGER_ID

All variables added? Continue...

### Step 4: Deploy

1. Click Deploy
2. Wait 2-3 minutes
3. Check logs for errors

- [ ] Deployment started
- [ ] Build completed
- [ ] Bot initialized successfully
- [ ] No connection errors

### Step 5: Verify Deployment

1. Get Railway URL from project
2. Update if needed in code
3. Bot should now be live 24/7

- [ ] Railway URL obtained
- [ ] Bot status is running
- [ ] Logs show no errors

---

## 🧪 Post-Deployment Testing

### Test Commands in Telegram

After deploying to Railway:

```
/start
/help
/play hello
/queue
/ask recommend music
```

- [ ] All commands work
- [ ] Bot responds quickly
- [ ] No errors in Railway logs

### Monitor Logs

In Railway dashboard:
- [ ] Check logs for errors
- [ ] Verify MongoDB connections
- [ ] Check ChatGPT responses

---

## 🎯 Success Indicators

Your bot is **ready for production** when:

- [x] All credentials obtained
- [x] .env file created and filled
- [x] Dependencies installed
- [x] Bot runs locally without errors
- [x] MongoDB connected successfully
- [x] Pyrogram client initialized
- [x] Telegram commands work
- [x] ChatGPT responds
- [x] Code pushed to GitHub
- [x] Deployed to Railway
- [x] Railway deployment successful
- [x] Bot responds 24/7
- [x] Logs show no errors
- [x] Ready for users!

---

## 🚨 Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution:**
```bash
pip install -r requirements.txt --upgrade
python main.py
```
- [ ] Issue resolved

### Issue: "Invalid MongoDB URI"
**Solution:**
1. Check MONGO_DB_URI in .env
2. Verify connection string format
3. Make sure IP is whitelisted in MongoDB Atlas
- [ ] Issue resolved

### Issue: "Invalid API key"
**Solution:**
1. Verify OPENAI_API_KEY in .env
2. No extra spaces
3. Key should start with `sk-`
4. Check key is not expired
- [ ] Issue resolved

### Issue: "Bot not connecting"
**Solution:**
1. Verify BOT_TOKEN is correct
2. Check internet connection
3. Restart bot
4. Check Railway logs
- [ ] Issue resolved

### Issue: "Pyrogram error"
**Solution:**
1. Verify STRING_SESSION is valid
2. Check API_ID and API_HASH
3. May need to regenerate session
- [ ] Issue resolved

---

## 📞 Getting Help

If you're stuck:

1. **Check Docs**: Look in `QUICK_START.md`
2. **Search Errors**: Google the error message
3. **Check Logs**: View full error in console
4. **Read TROUBLESHOOTING**: See sections above
5. **Join Support**: https://t.me/song_assistant

---

## 🎉 Final Checklist

- [ ] All documentation read
- [ ] All credentials gathered
- [ ] .env file created and verified
- [ ] Dependencies installed
- [ ] Bot tested locally (all commands work)
- [ ] Code pushed to GitHub
- [ ] Deployed to Railway
- [ ] Railway deployment successful
- [ ] Live bot working 24/7
- [ ] Ready to share with users!

---

## 🏁 You're Done!

Your Music Bot is now:
✅ Running on Railway  
✅ Using ChatGPT AI  
✅ Storing data in MongoDB  
✅ Streaming via Pyrogram  
✅ Ready for production  

**Congratulations!** 🎵🚀

---

**Marked Complete Date**: _______________  
**Bot Status**: ☐ Local | ☐ Railway | ✅ Production

**Keep this checklist for future reference!**
