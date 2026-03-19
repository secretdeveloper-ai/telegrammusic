# 🚀 Updated Setup - ChatGPT + MongoDB + Pyrogram

This guide covers the new setup with:
- **ChatGPT/GPT-4** instead of Claude
- **MongoDB** for data persistence instead of JSON files
- **Pyrogram** string session for assistant account music streaming
- Private bot configuration

## 🔑 Your Credentials (Already Configured)

All your credentials are already added to the `.env.example` file:

```env
# Telegram
BOT_TOKEN=8680937067:AAE885EaAnQ5S0Ik9BtJYgbgPEtJb0poJF4
OWNER_ID=your_telegram_id
LOGGER_ID=-1003858465326

# Pyrogram (String Session)
API_ID=31656328
API_HASH=a9e57623a4408a41418ca647b2f08950
STRING_SESSION=BACcYO4Aw...

# MongoDB (Already configured)
MONGO_DB_URI=mongodb+srv://aditya0:aditya0@cluster0.9m8897t.mongodb.net/?appName=Cluster0

# Support
SUPPORT_CHAT=https://t.me/song_assistant
BOT_NAME=MUSIC BOT
```

## 📝 What You Still Need

1. **OpenAI API Key** - For ChatGPT
   - Get from: https://platform.openai.com/api-keys
   - Add to `.env` as `OPENAI_API_KEY`

2. **Optional: Spotify Credentials**
   - Client ID & Secret for better music search
   - From: https://developer.spotify.com/dashboard

## ⚡ Quick Setup

### Windows
```bash
cd telegram-music-bot
setup.bat
# Edit .env with your OPENAI_API_KEY
python main.py
```

### Mac/Linux
```bash
cd telegram-music-bot
./setup.sh
# Edit .env with your OPENAI_API_KEY
python main.py
```

## 🎯 Key Features Now

✅ **ChatGPT Integration**
- Smart song recommendations
- Natural language processing
- `/ask` command for AI assistance

✅ **MongoDB Backend**
- Cloud database for group settings
- Queue persistence
- User data storage
- No JSON file conflicts

✅ **Pyrogram String Session**
- Assistant account joins groups
- Direct music streaming capability
- Better privacy control
- Multi-account support

✅ **Private Bot**
- Your credentials kept safe
- No sharing needed
- Personal use only
- Logger channel for monitoring

## 🏗️ Architecture

```
Telegram Bot
    ↓
Telegram API
    ↓
python-telegram-bot (Handler layer)
    ↓
├── Music Fetcher (YouTube/Spotify)
├── GPT Assistant (ChatGPT)
├── Mongo Group Manager (MongoDB)
├── Mongo Queue Manager (MongoDB)
└── Pyrogram Client (String Session)
    ↓
Database: MongoDB Atlas
```

## 📊 MongoDB Collections

The bot automatically creates these collections:

1. **groups** - Group settings, admins, bans, stats
2. **queues** - Music queues for each group
3. **users** - User preferences and history

## 🎤 Pyrogram Assistant Account

Your bot now has a Pyrogram account that can:
- Join groups via your string session
- Stream music directly
- Send rich media
- Manage group settings

The `STRING_SESSION` is your authenticated session key - **keep it private!**

## 🔒 Security Notes

⚠️ **CRITICAL**
- Never share `.env` file
- Never commit `.env` to GitHub
- Keep STRING_SESSION secret
- Use Railway's secret management
- Regenerate credentials if exposed

## 🚀 Deployment to Railway

1. **Create GitHub Repository**
   ```bash
   git init
   git add .
   git commit -m "Setup with ChatGPT and MongoDB"
   git push
   ```

2. **Connect to Railway**
   - Go to railway.app
   - Create new project from GitHub repo

3. **Set Environment Variables**
   - Add all `.env` variables to Railway
   - Especially: `OPENAI_API_KEY`, `BOT_TOKEN`, `STRING_SESSION`

4. **Deploy**
   - Railway auto-builds from Dockerfile
   - Bot connects to MongoDB Atlas automatically

## 🧪 Testing

```bash
# Start bot
python main.py

# In Telegram, test:
/start
/help
/ask What is music?
/play hello world
/queue
```

## 📱 Admin Commands (New)

```
/info              - Show group information
/admin_add <id>    - Add admin
/admin_remove <id> - Remove admin
/ban <id>          - Ban user
/unban <id>        - Unban user
/set_prefix <char> - Change prefix
/queue_limit <num> - Set queue limit
```

## 🛠️ Troubleshooting

### "MongoDB connection failed"
- Check MONGO_DB_URI is correct
- Verify IP address is whitelisted in MongoDB Atlas
- Check network connection

### "Pyrogram startup error"
- STRING_SESSION might be expired
- Regenerate using: https://pyrogram.org/docs/intro/install
- Verify API_ID and API_HASH

### "ChatGPT not responding"
- Verify OPENAI_API_KEY is valid
- Check API usage limits
- Ensure account has credits

### "Bot not receiving messages"
- Check BOT_TOKEN is correct
- Verify bot privacy settings in BotFather
- Check Telegram webhook URL

## 🎵 Commands Reference

**Music:**
`/play` `/ next` `/ skip` `/ queue` `/ shuffle` `/ remove` `/clear_queue`

**Admin:**
`/init` `/info` `/admin_add` `/admin_remove` `/ban` `/unban` `/set_prefix` `/queue_limit`

**Utility:**
`/start` `/help` `/ask` `/stats` `/about`

## 📚 Additional Resources

- **Pyrogram Docs**: docs.pyrogram.org
- **OpenAI API**: platform.openai.com
- **MongoDB Atlas**: mongodb.com/cloud/atlas
- **Telegram Bot API**: core.telegram.org/bots
- **Railway Docs**: docs.railway.app

## 🤝 Support

- Support Chat: https://t.me/song_assistant
- Logger Channel: -1003858465326
- Issue tracking: Create GitHub issues

## ✅ Checklist Before Going Live

- [ ] OpenAI API key added
- [ ] MongoDB URI verified
- [ ] Pyrogram STRING_SESSION valid
- [ ] Bot token correct
- [ ] Support chat linked
- [ ] Logger channel set
- [ ] All `.env` variables configured
- [ ] Tested locally with `/start` and `/play`
- [ ] Pushed to GitHub
- [ ] Railway deployment successful
- [ ] MongoDB indexes created
- [ ] Pyrogram client connected

---

**You're all set!** Your bot is now:
- 🤖 Powered by ChatGPT
- 📦 Using MongoDB database
- 🎤 Ready with Pyrogram streaming
- 🔒 Private and secure
- ☁️ Ready for Railway deployment

Happy coding! 🎵
