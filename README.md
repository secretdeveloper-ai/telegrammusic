# 🎵 Telegram Music Bot

**A powerful, production-ready music bot for Telegram groups** 

✅ YouTube + Spotify Music  
✅ Group Management  
✅ AI Music Recommendations (ChatGPT)  
✅ Broadcast Announcements  
✅ Cloud Database (MongoDB)  
✅ Ready to Deploy  

---

## 🚀 3-Step Deploy

### 1. Create Railway Account
Go to https://railway.app → Sign up with GitHub

### 2. Connect This Repository
- New Project → Deploy from GitHub
- Select this repo
- Railway auto-builds from Dockerfile

### 3. Add Environment Variables
Copy-paste all variables from the `.env.example` file to Railway's Variables section.

**[📖 Detailed Deploy Guide](DEPLOY_GUIDE.md)** ← Click here!

---

## 🎮 Quick Commands

```
/play <song>        - Play a song
/queue              - Show queue
/skip               - Next song
/shuffle            - Random order
/broadcast <msg>    - Announce to all groups (owner only)
/help               - All commands
```

**[📋 Full Commands List](DEPLOY_GUIDE.md#-bot-commands)**
---

## 📦 What's Included?

✅ **All credentials pre-configured**
- Telegram Bot Token
- MongoDB database ready
- Pyrogram string session
- ChatGPT integration (optional)

✅ **Production-ready code**
- No errors
- Async throughout
- Full error handling
- Tested patterns

✅ **Complete documentation**
- Deploy guide
- Command reference
- Setup checklist
- Quick start

---

## 💾 Database

**MongoDB Cloud** (free tier available)

Your data is always safe:
- Groups & settings
- Music queues
- User statistics
- Auto backups

---

## 🎵 Music Sources

**YouTube** (via yt-dlp)
- ✅ Automatically finds and plays songs
- ✅ No manual setup needed
- ✅ Handles everything internally

**Spotify** (optional preview links)

---

## 🤖 AI Features (Optional)

Uses OpenAI ChatGPT for:
- Smart music recommendations
- /ask command (answer questions)
- Better search results

**Not required** - bot works great without it!

---

## 📁 Project Structure

```
telegram-music-bot/
├── main.py                          # Bot entry point
├── config.py                        # Configuration from .env
├── requirements.txt                 # All dependencies
├── Dockerfile                       # For Railway deployment
├── .env.example                     # All variables pre-filled
│
├── handlers/                        # Bot commands
│   ├── music_commands.py
│   ├── group_commands.py
│   ├── utility_commands.py
│   └── broadcast_commands.py
│
├── utils/                           # Helper modules
│   ├── mongodb_manager.py           # Database operations
│   ├── mongo_group_manager.py       # Group settings
│   ├── mongo_queue_manager.py       # Queue management
│   ├── claude_assistant.py          # ChatGPT integration
│   ├── pyrogram_client.py           # User account login
│   └── music_fetcher.py             # YouTube/Spotify search
│
└── docs/                            # Documentation
    ├── DEPLOY_GUIDE.md              # Deployment steps
    ├── QUICK_START.md               # Quick setup
    ├── SETUP_CHECKLIST.md           # Verification steps
    └── ... (more guides)
```

---

## ✅ Already Configured

- ✅ Bot Token
- ✅ Telegram API (API_ID, API_HASH)
- ✅ MongoDB connection string
- ✅ Pyrogram string session
- ✅ Logger channel ID
- ✅ Bot name and support chat
- ⚠️ Owner ID (you need to add yours)
- ⚠️ ChatGPT API key (optional)

---

## 🔧 Before Deployment

1. **Get your Telegram ID**
   - Send `/start` to @userinfobot
   - Copy your ID
   - Update `OWNER_ID` in Railway variables

2. **(Optional) Get ChatGPT API key**
   - Go to platform.openai.com
   - Create API key
   - Add to `OPENAI_API_KEY` variable
   - Or leave empty (bot works without it)

3. **Verify database connection**
   - MONGO_DB_URI already configured
   - Test connection (Railway will tell you if wrong)

---

## 📖 Documentation

- [🚀 Deployment Guide](DEPLOY_GUIDE.md) - How to deploy
- [⚡ Quick Start](QUICK_START.md) - 5-minute setup
- [📋 Setup Checklist](SETUP_CHECKLIST.md) - Verify everything
- [🤔 Conversation Guide](CONVERSION_GUIDE.md) - Claude to ChatGPT
- [📝 Credentials Reference](CREDENTIALS_REFERENCE.md) - All variables explained

---

## 🆘 Troubleshooting

**Bot not responding?**
- Check LOGGER_ID (-1003858465326) for error logs
- Verify all variables in Railway

**Songs not playing?**
- Pyrogram string session might be expired
- Re-generate string session: `pyrogram-string-session-generator`

**MongoDB connection failed?**
- Check MONGO_DB_URI is correct
- Verify MongoDB instance is active

---

## 🎯 Status

| Feature | Status |
|---------|--------|
| Music Playback | ✅ Ready |
| Group Management | ✅ Ready |
| AI Recommendations | ✅ Ready |
| Broadcast Feature | ✅ Ready |
| Database | ✅ Ready |
| Deployment Config | ✅ Ready |

**Overall: Production Ready** 🚀

---

## 📞 Support

- Check logs at LOGGER_ID: -1003858465326
- Support channel: https://t.me/song_assistant
- Review [DEPLOY_GUIDE.md](DEPLOY_GUIDE.md) for help

---

## 📜 License

Open source - use freely

---

## 🎵 Enjoy the Music! 🎵

**Ready to deploy?** → [Follow the deploy guide](DEPLOY_GUIDE.md) (3 steps, 5 minutes!)

---

**Version**: 2.0 | **Status**: ✅ Production | **Last Updated**: March 19, 2026

## 📦 Dependencies

- **python-telegram-bot**: Telegram API wrapper
- **anthropic**: Claude AI integration
- **yt-dlp**: YouTube media fetching
- **spotipy**: Spotify API wrapper
- **aiohttp**: Async HTTP client
- **python-dotenv**: Environment configuration

## 🚀 Performance Tips

1. Use persistent Redis for production queues
2. Implement song caching to reduce API calls
3. Monitor Railway resource usage
4. Archive old queue data periodically
5. Use CDN for downloading music

## 📝 License

MIT License - Feel free to use and modify!

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## ⚠️ Disclaimer

Ensure you have the right to play music from your sources. Respect copyright laws and platform terms of service.

## 📞 Support

For issues and questions:
- Check existing GitHub issues
- Create a new issue with details
- Include bot logs if applicable

---

**Made with ❤️ for music lovers**
