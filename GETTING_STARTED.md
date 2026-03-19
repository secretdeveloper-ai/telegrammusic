# 🎬 Getting Started - Complete Guide

Welcome! This guide explains how to get all necessary credentials and run your Music Bot.

## 📋 Overview

Your bot needs these credentials:
1. **Telegram Bot Token** - From Telegram BotFather
2. **Anthropic API Key** - From Anthropic Console (for Claude AI)
3. **Spotify Credentials** (Optional) - For Spotify music
4. **YouTube API** (Optional) - For better YouTube search

## 🤖 1. Telegram Bot Token

### Get Your Bot Token

1. **Open Telegram** and search for `@BotFather`
2. **Start Chat** - Send `/start`
3. **Create Bot** - Send `/newbot`
4. **Follow Prompts:**
   - Enter bot name: `Music Bot`
   - Enter bot username: `mymusic_bot` (must be unique with `_bot` suffix)
5. **Copy Token** - You'll get something like:
   ```
   123456789:ABCDefGHIjklMnOpQrStUvWxYz
   ```
6. **Save It** - Add to your `.env` file as `TELEGRAM_BOT_TOKEN`

### Test Your Token

```bash
curl https://api.telegram.org/bot<YOUR_TOKEN>/getMe
```

## 🔑 2. Anthropic API Key

### Get Your API Key

1. **Go to** [console.anthropic.com](https://console.anthropic.com)
2. **Sign Up/Log In** - Create account if needed
3. **Go to API Keys** section (usually in settings)
4. **Create New Key** - Click "Create API Key"
5. **Copy Key** - It looks like: `sk-ant-xxxxxxxxxxxxx`
6. **Save It** - Add to `.env` as `ANTHROPIC_API_KEY`

### Pricing

- **Free Trial**: $5 credit (usually enough for testing)
- **Pay as you go**: ~$0.80 per 1M input tokens
- For casual use: ~$1-5/month

### Verify Key

```bash
curl https://api.anthropic.com/v1/models \
  -H "api-key: <YOUR_API_KEY>"
```

## 🎵 3. Spotify (Optional but Recommended)

### Get Spotify Credentials

1. **Go to** [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)
2. **Log In/Sign Up** - Free account (no payment needed!)
3. **Create App** - Click "Create an App"
4. **Accept Terms** - Check boxes and create
5. **Get Credentials:**
   - Copy `Client ID` → `SPOTIFY_CLIENT_ID`
   - Click "Show Client Secret" → Copy → `SPOTIFY_CLIENT_SECRET`

### Add to .env

```env
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
```

## 🎬 4. YouTube API (Optional)

### Enable YouTube Data API

1. **Go to** [console.cloud.google.com](https://console.cloud.google.com)
2. **Create New Project**
3. **Search for "YouTube Data API"**
4. **Enable it** - Click "Enable"
5. **Create Credentials:**
   - Type: API Key
   - Restriction: YouTube Data API v3
6. **Copy Key** → `YOUTUBE_API_KEY` in `.env`

### Pricing

- Free: 10,000 requests/day
- Usually sufficient for one bot

## ⚙️ Setting Up .env File

1. **Copy Template**
   ```bash
   cp .env.example .env
   ```

2. **Edit .env** with your editor
   ```bash
   # On Windows
   code .env
   # Or use Notepad:
   notepad .env
   ```

3. **Fill in Your Credentials**
   ```env
   # Required
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   ANTHROPIC_API_KEY=your_api_key_here

   # Recommended
   SPOTIFY_CLIENT_ID=your_spotify_id
   SPOTIFY_CLIENT_SECRET=your_spotify_secret

   # Optional
   YOUTUBE_API_KEY=your_youtube_key

   # For local testing
   TELEGRAM_WEBHOOK_URL=
   DEBUG=True
   ```

## 🚀 Running Locally

### Windows Users

1. **Run Setup Script**
   ```bash
   setup.bat
   ```

2. **After setup, activate venv (if needed)**
   ```bash
   venv\Scripts\activate
   ```

3. **Run Bot**
   ```bash
   python main.py
   ```

### Mac/Linux Users

1. **Run Setup Script**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Activate Virtual Environment**
   ```bash
   source venv/bin/activate
   ```

3. **Run Bot**
   ```bash
   python main.py
   ```

## 🌐 Railway Deployment

Once working locally, deploy to Railway:

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial bot"
   git push
   ```

2. **Follow** `RAILWAY_DEPLOY.md` guide

3. **Set variables** in Railway dashboard with same credentials

## ✅ Testing Your Bot

1. **Bot Should Show:**
   ```
   🎵 Starting Music Bot...
   🔄 Starting with polling...
   ```

2. **Add to Telegram:**
   - Search for your bot username
   - Click "/start"
   - Send "/help"

3. **Try Commands:**
   ```
   /play hello world
   /queue
   /help
   ```

## 🐛 Common Issues

### "Invalid Telegram Token"
- Check you copied the FULL token
- No extra spaces or characters
- Try `/getMe` test command above

### "Invalid Anthropic API Key"
- Key should start with `sk-ant-`
- Check it's not expired
- Generate new key if needed

### "Music not playing"
- Verify Spotify/YouTube credentials
- Check internet connection
- Try with both sources

### Bot not responding
- Check if bot is running (`python main.py`)
- Verify `.env` file loaded
- Check terminal for error messages

## 💡 Tips

- **Keep credentials safe** - Never share `.env` file
- **Use Railway secrets** - Don't manually paste in code
- **Start with polling** - Easier than webhooks for testing
- **Test locally first** - Before deploying to Railway
- **Monitor API usage** - Check free tier limits
- **Join bot testing group** - Test with more people

## 📚 Resources

- **Telegram Bot Docs**: [core.telegram.org/bots](https://core.telegram.org/bots)
- **Anthropic Docs**: [anthropic.com/docs](https://anthropic.com/docs)
- **Spotify API**: [developer.spotify.com](https://developer.spotify.com)
- **Railway Docs**: [docs.railway.app](https://docs.railway.app)

## 🆘 Need Help?

1. Check error messages in terminal
2. Review README.md
3. Check RAILWAY_DEPLOY.md for deployment issues
4. Verify all credentials are correct
5. Try bot with just Telegram (no music) first

---

**Ready?** Start with:
```bash
# Windows
setup.bat

# Mac/Linux
./setup.sh

# Then
python main.py
```

Good luck! 🎵
