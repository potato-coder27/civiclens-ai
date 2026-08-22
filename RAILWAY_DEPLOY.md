# Railway.app Deployment Guide for CivicLens AI

## Quick Deploy to Railway

### Option 1: Deploy with GitHub (Recommended)

1. **Push to GitHub**
```bash
git remote add origin https://github.com/YOUR-USERNAME/civiclens-ai.git
git branch -M main
git push -u origin main
```

2. **Go to Railway.app**
   - Visit https://railway.app
   - Click "New Project"
   - Select "Deploy from GitHub"
   - Connect your GitHub account
   - Select `civiclens-ai` repository
   - Click Deploy

3. **Configure Services**
   - Railway will auto-detect and deploy
   - Set environment variables if needed
   - Services will be accessible via Railway domains

---

### Option 2: Deploy with Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Create new project
railway init

# Deploy
railway up
```

---

## Environment Variables (Optional)

Add to Railway dashboard under Variables:
```
PORT=8000
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

---

## Accessing Your Deployed App

After deployment, Railway provides URLs:

- **Streamlit App:** `https://your-app.railway.app`
- **API (if configured):** `https://api.your-app.railway.app`
- **API Docs:** `https://api.your-app.railway.app/docs`

---

## Multiple Services Deployment

For both Streamlit + FastAPI on the same Railway project:

### Create `railway.json`
```json
{
  "services": {
    "streamlit": {
      "build": "streamlit run app.py --server.port=$PORT",
      "ports": [8501]
    },
    "api": {
      "build": "python api.py",
      "ports": [8000]
    }
  }
}
```

---

## Docker Deployment

Railway also supports Docker. Your `Dockerfile` will:
1. Use Python 3.10
2. Install dependencies
3. Run Streamlit on port 8501

---

## Cost

- **Railway Free Tier:** $5/month credit
- **CivicLens AI monthly usage:** ~$2-3 (under free tier)

---

## Troubleshooting

**App crashes on startup?**
- Check logs: Railway dashboard → Logs
- Verify all imports work: `python -c "import database; import ai_analyzer"`

**Port already in use?**
- Railway automatically assigns ports
- Use Railway's provided domain

**Database issues?**
- SQLite works in Railway
- Data persists during deployments
- Back up `data/civiclens.db` to GitHub if needed

---

## Next Steps

1. Push code to GitHub
2. Go to https://railway.app
3. Click "New Project" → "Deploy from GitHub"
4. Select your repo
5. Click Deploy
6. Get your live URL in 2-3 minutes

**You're done! 🎉**
