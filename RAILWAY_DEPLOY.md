# 🚀 Railway Deployment Guide

This guide walks you through deploying your Telegram Music Bot to Railway for free.

## Prerequisites

- GitHub account (for repository)
- Railway account (free at [railway.app](https://railway.app))
- Telegram bot token
- Anthropic API key

## Step 1: Prepare Your Code

1. **Create GitHub Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Telegram Music Bot"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/telegram-music-bot.git
   git push -u origin main
   ```

2. **Verify All Files Are Included**
   - `main.py`
   - `config.py`
   - `requirements.txt`
   - `Dockerfile`
   - `.env.example`
   - `handlers/` directory
   - `utils/` directory

## Step 2: Set Up Railway Project

1. **Log into Railway**
   - Go to [railway.app](https://railway.app)
   - Sign up or log in with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Connect your GitHub account
   - Select the `telegram-music-bot` repository

3. **Configure Build Settings**
   - Railway auto-detects `Dockerfile`
   - No additional build configuration needed
   - Deploy button appears automatically

## Step 3: Set Environment Variables

1. **In Railway Dashboard**
   - Go to your project
   - Click "Variables" tab
   - Add the following:

   ```
   TELEGRAM_BOT_TOKEN = your_bot_token_from_botfather
   ANTHROPIC_API_KEY = your_anthropic_api_key
   SPOTIFY_CLIENT_ID = your_spotify_client_id
   SPOTIFY_CLIENT_SECRET = your_spotify_client_secret
   TELEGRAM_WEBHOOK_URL = (will get this after deployment)
   WEBHOOK_PORT = 8080
   DEBUG = False
   ```

2. **Get Webhook URL**
   - After first deployment, Railway generates a public URL
   - Format: `https://your-app-name.railway.app`
   - Add this as `TELEGRAM_WEBHOOK_URL`

## Step 4: Deploy

1. **Initial Deploy**
   - Click "Deploy" button in Railway dashboard
   - Wait for build to complete (2-5 minutes)
   - Check logs for any errors

2. **Verify Deployment**
   ```bash
   # View logs in Railway dashboard
   # The bot should show: "🎵 Starting Music Bot..."
   # and "🌐 Starting with webhook: https://..."
   ```

## Step 5: Test Your Bot

1. **Add Bot to Telegram Group**
   - Search for your bot on Telegram
   - Click `/start`
   - Add to group

2. **Test Commands**
   ```
   /help           # Should show command list
   /play test      # Try playing a song
   /queue          # Check queue
   ```

## Free Tier Limits

Railway offers a **free tier with $5 credit/month**:

✅ Sufficient for:
- Usually covers 1-2 bots running continuously
- Reasonable API usage
- Good for development/testing

⚠️ If exceeded:
- Service temporarily pauses
- Resumes on next billing cycle
- Consider paid tier for production

## Cost Optimization

1. **Use Webhook Instead of Polling**
   - More efficient than polling
   - Already configured in the bot

2. **Monitor Resource Usage**
   - Check Railway dashboard regularly
   - View memory and CPU usage
   - Optimize if necessary

3. **Database Storage**
   - Current setup uses JSON files
   - Fine for small groups
   - Consider PostgreSQL add-on for scale

## Troubleshooting

### Bot Not Starting

**Error in logs:**
```
ModuleNotFoundError: No module named 'telegram'
```
**Solution:**
- Check `requirements.txt` is in root directory
- Railway needs to find it during build

### Telegram Webhook Errors

**Bot not receiving messages:**
```
Problem: Webhook not responding
```
**Solution:**
1. Verify `TELEGRAM_WEBHOOK_URL` is correct
2. Check bot logs in Railway
3. Ensure WEBHOOK_PORT=8080

### API Key Issues

**Error: "Invalid API Key"**
- Double-check your keys in Environment Variables
- No extra spaces or quotes
- Verify keys are valid and not expired

### Out of Memory

**Error: "Memory limit exceeded"**
- Railway free tier has limits
- Reduce queue limits: `/queue_limit 30`
- Clear old data periodically
- Consider paid tier

## Updating Your Bot

1. **Make Code Changes Locally**
   ```bash
   # Edit files as needed
   git add .
   git commit -m "Update: Feature description"
   git push origin main
   ```

2. **Auto-Redeploy**
   - Railway watches your GitHub repo
   - Automatically rebuilds and deploys
   - Check logs to verify deployment

## Monitoring & Maintenance

### View Logs
- In Railway dashboard, select your service
- Click "Logs" tab
- Search for errors or specific messages

### Monitor Usage
- Dashboard shows memory/CPU usage
- Current month's billing
- Service uptime

### Regular Maintenance
- Archive old queue data monthly
- Review banned users list
- Update dependencies (run `pip update -r requirements.txt`)
- Check for bot messages/warnings

## Advanced: Railway CLI

For more control, use Railway CLI:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link project
railway link your-project-id

# Deploy
railway up

# View logs
railway logs

# Set variables
railway variables set KEY=VALUE
```

## Free Alternatives to Consider

If Railway limit is exceeded:
- **Heroku** (no free tier as of 2024)
- **Replit** (limited resources)
- **Google Cloud Run** (generous free tier)
- **AWS Lambda** (complex setup)

## Support & Resources

- Railway Docs: [docs.railway.app](https://docs.railway.app)
- Telegram Bot API: [core.telegram.org/bots](https://core.telegram.org/bots)
- Anthropic Docs: [anthropic.com/docs](https://anthropic.com/docs)

---

**Your bot should now be live! 🎉**

Add your bot to groups and start playing music!
