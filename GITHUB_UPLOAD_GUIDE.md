# 📤 GitHub Upload Checklist

Follow these 5 steps to upload your bot to GitHub!

---

## ✅ Step 1: Create GitHub Account (if you don't have)
- Go to https://github.com/signup
- Sign up with email
- Verify email

---

## ✅ Step 2: Create New Repository

**On GitHub.com:**
1. Click `+` (top right) → "New repository"
2. **Repository name**: `telegram-music-bot`
3. **Description**: "A powerful music bot for Telegram"
4. **Public** (so Railway can access it)
5. **Add .gitignore**: Select "Python"
6. Click "Create repository"

**You'll see:**
```
Quick setup — if you've done this kind of thing before
```

---

## ✅ Step 3: Upload Files to GitHub

**Option A: Command Line (Easy)**

On your computer, open PowerShell/Terminal in your project folder:

```powershell
# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Music bot ready"

# Add remote (copy from GitHub page)
git remote add origin https://github.com/YOUR_USERNAME/telegram-music-bot.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Option B: GitHub Desktop (Easier)**
1. Download GitHub Desktop: https://desktop.github.com
2. Click "Add Local Repository"
3. Select your `telegram-music-bot` folder
4. Click "Publish repository"
5. Upload files

**Option C: Web Upload (Easiest)**
1. On GitHub repo page, click "Add file" → "Upload files"
2. Drag your files
3. Commit

---

## ✅ Step 4: Verify Upload

**Check GitHub:**
1. Go to your repo: https://github.com/YOUR_USERNAME/telegram-music-bot
2. You should see:
   - `main.py`
   - `config.py`
   - `Dockerfile`
   - `requirements.txt`
   - `.env.example`
   - `handlers/` folder
   - `utils/` folder
   - `README.md`

---

## ✅ Step 5: Deploy on Railway

**Now the fun part!**

1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub"
5. **Select this repo**: `telegram-music-bot`
6. Confirm deploy

---

## ⚠️ Important: Add Variables BEFORE Deploy

**When Railway asks for variables:**
1. Copy all from `.env.example`
2. Paste into Railway Variables tab
3. Update `OWNER_ID` with your Telegram ID
4. Save

---

## 🎉 Done!

Your bot is now:
- ✅ On GitHub (backed up, easy to update)
- ✅ Deployed on Railway (24/7 running)
- ✅ Ready to use!

Watch the Railway logs to see it starting up. Should say:

```
Bot running...
MongoDB connected!
Pyrogram authenticated!
```

---

## 🔄 Later Updates

If you make changes locally:

```powershell
# Make changes in your code

# Upload them
git add .
git commit -m "Update: your description"
git push

# Railway auto-deploys! (no need to do anything)
```

---

## 🆘 Common Issues

**"Push failed"?**
- Make sure you setup git correctly
- Run: `git config --global user.email "your@email.com"`
- Run: `git config --global user.name "Your Name"`

**Railway not deploying?**
- Check if repo is public (not private)
- Refresh Railway page
- Check Railway logs for errors

**Bot not starting?**
- Verify OWNER_ID is set
- Check all variables match `.env.example`
- Look at Railway logs

---

## 📞 Need Help?

- **GitHub Issues**: Use the repo's Issues tab to track problems
- **Railway Logs**: Click "View Logs" in Railway dashboard
- **Your Logger Channel**: -1003858465326 shows real-time bot errors

---

**That's it! 🎉 Your bot is live!**

