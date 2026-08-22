# 🚀 Deployment Guide — CivicLens AI on Streamlit Cloud

Deploy your CivicLens AI app to the internet **for free** in 5 minutes!

## ✅ Prerequisites

- ✅ GitHub account (create at [github.com](https://github.com))
- ✅ Streamlit account (create at [streamlit.io](https://streamlit.io))
- ✅ Code pushed to GitHub (already done!)

---

## 📋 Step 1: Push Code to GitHub

Your project is already in git. Now push it to GitHub:

```bash
cd c:\Users\HP\.gemini\antigravity\scratch\civiclens-ai

# Set your GitHub username and email
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR-USERNAME/civiclens-ai.git
git branch -M main
git push -u origin main
```

> Replace `YOUR-USERNAME` with your actual GitHub username

---

## 🎯 Step 2: Deploy to Streamlit Cloud

1. **Go to** [share.streamlit.io](https://share.streamlit.io)
2. **Click** "New app" button
3. **Select**:
   - Repository: `YOUR-USERNAME/civiclens-ai`
   - Branch: `main`
   - Main file path: `app.py`
4. **Click** "Deploy"

Streamlit will:
- Clone your repo
- Install dependencies from `requirements.txt`
- Run `streamlit run app.py`
- Generate a public URL like: `https://civiclens-ai-YOUR-USERNAME.streamlit.app`

✅ **Your app is now live!** Share the link with anyone.

---

## 📝 Step 3: Access Features

Once deployed, anyone can:
- ✅ Access from any browser (Chrome, Firefox, Safari, Edge)
- ✅ Upload images and photos
- ✅ View AI analysis instantly
- ✅ See interactive dashboard with charts
- ✅ Export PDF reports

---

## 🔄 Updates & Redeployment

To push changes to your live app:

```bash
# Make changes to your files
# Then commit and push:
git add .
git commit -m "Update: new feature or bugfix"
git push origin main
```

Streamlit Cloud automatically redeploys within 1-2 minutes! 🎉

---

## ⚙️ Configuration

Your `.streamlit/config.toml` file is already configured for:
- ✅ Dark theme (matches your design)
- ✅ File upload support (up to 200 MB)
- ✅ CORS protection enabled
- ✅ No usage stats collection

---

## 🆘 Troubleshooting

**"ModuleNotFoundError" after deployment?**
- Check that all imports in your Python files match packages in `requirements.txt`
- Restart the app in Streamlit Cloud settings

**"File not found" errors?**
- Use relative paths: `data/uploads/` not `C:\Users\...`
- Database and uploads are stored in Streamlit's filesystem

**Custom domain?**
- Streamlit Cloud free tier doesn't support custom domains
- Upgrade to Pro plan for custom domains

---

## 📊 Sharing the App

Your live app URL is: **`https://civiclens-ai-YOUR-USERNAME.streamlit.app`**

Share it via:
- 📱 Direct link
- 📧 Email
- 📎 QR code (Streamlit Cloud generates one)
- 🐦 Social media

---

## 🎓 Next Steps (Optional)

- Add authentication (use `streamlit-authenticator`)
- Connect to PostgreSQL for production database
- Add email notifications for reports
- Integrate Google Cloud Vision API for real AI
- Custom domain (Streamlit Pro plan)

---

**Questions?** See [Streamlit Cloud Docs](https://docs.streamlit.io/deploy/streamlit-community-cloud)
