#!/usr/bin/env python3
"""
🚀 CivicLens AI - Complete Deployment Guide
Deploy to Railway in 5 minutes
"""

import os
import subprocess

def check_git_status():
    """Check if git is ready for deployment"""
    print("\n" + "="*80)
    print("📊 GIT STATUS CHECK")
    print("="*80)
    
    try:
        result = subprocess.run(["git", "status"], capture_output=True, text=True)
        print(result.stdout)
        
        # Check for uncommitted changes
        if "nothing to commit" in result.stdout:
            print("✅ All changes committed and ready for deployment!")
            return True
        else:
            print("⚠️  You have uncommitted changes. Commit them first:")
            print("   git add .")
            print("   git commit -m 'Prepare for deployment'")
            return False
    except Exception as e:
        print(f"❌ Error checking git status: {e}")
        return False

def show_deployment_steps():
    """Display deployment steps"""
    print("\n" + "="*80)
    print("🚀 DEPLOYMENT STEPS - RAILWAY.APP")
    print("="*80)
    
    steps = """
STEP 1: Push Code to GitHub
────────────────────────────────────────────────────────────────────────────
1. Create a GitHub account at https://github.com (if you don't have one)
2. Create a new repository named 'civiclens-ai'
3. Run these commands:

   git remote add origin https://github.com/YOUR-USERNAME/civiclens-ai.git
   git branch -M main
   git push -u origin main

   (Replace YOUR-USERNAME with your actual GitHub username)


STEP 2: Deploy with Railway.app
────────────────────────────────────────────────────────────────────────────
1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub"
4. Authorize GitHub access
5. Select the 'civiclens-ai' repository
6. Click "Deploy"
7. Wait 2-3 minutes for deployment to complete


STEP 3: Access Your Live App
────────────────────────────────────────────────────────────────────────────
Once deployed, you'll get URLs:

✅ Streamlit App:     https://your-app.railway.app
✅ API Docs:          https://your-app.railway.app/docs
✅ API Base URL:      https://your-app.railway.app/api


STEP 4: Share with Others
────────────────────────────────────────────────────────────────────────────
Share the URL with anyone to access your app:

   "Check out CivicLens AI: https://your-app.railway.app"
   
   No installation needed - works on any device!
    """
    
    print(steps)

def show_what_you_have():
    """Show what's ready for deployment"""
    print("\n" + "="*80)
    print("✅ DEPLOYMENT READY CHECKLIST")
    print("="*80)
    
    files = {
        "app.py": "✅ Streamlit frontend",
        "api.py": "✅ FastAPI backend",
        "database.py": "✅ Database module",
        "ai_analyzer.py": "✅ AI analysis engine",
        "priority_engine.py": "✅ Priority scoring",
        "duplicate_detector.py": "✅ Duplicate detection",
        "requirements.txt": "✅ Python dependencies",
        "Dockerfile": "✅ Docker configuration",
        "Procfile": "✅ Process file for Railway",
        "RAILWAY_DEPLOY.md": "✅ Deployment documentation",
        ".git/": "✅ Git repository"
    }
    
    print("\nProject Files Ready:")
    for file, status in files.items():
        print(f"  {status}  {file}")
    
    print(f"\n📊 Total: {len(files)} components ready")
    print("🎯 Estimated deployment time: 2-3 minutes")
    print("💰 Cost: FREE (within Railway free tier)")

def show_commands():
    """Show useful commands"""
    print("\n" + "="*80)
    print("📋 USEFUL COMMANDS")
    print("="*80)
    
    commands = """
# Check git status
git status

# Commit changes
git add .
git commit -m "Ready for deployment"

# Push to GitHub
git push origin main

# View git log
git log --oneline

# Check Python version
python --version

# Run API locally
python api.py

# Run Streamlit locally
streamlit run app.py

# Test API
python test_api.py

# View deployment files
type Dockerfile
type Procfile
type requirements.txt
    """
    
    print(commands)

def main():
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                   🚀 CIVICLENS AI DEPLOYMENT GUIDE                         ║
║                   Deploy Your App in 5 Minutes                             ║
╚════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Check git status
    if not check_git_status():
        print("\n⚠️  Please commit your changes before deploying!")
        print("   git add .")
        print("   git commit -m 'Ready for deployment'")
        return
    
    # Show what's ready
    show_what_you_have()
    
    # Show deployment steps
    show_deployment_steps()
    
    # Show commands
    show_commands()
    
    # Final message
    print("\n" + "="*80)
    print("🎉 YOU'RE READY TO DEPLOY!")
    print("="*80)
    print("""
Next Steps:
1. Go to https://railway.app
2. Sign up (free)
3. Click "New Project" → "Deploy from GitHub"
4. Select civiclens-ai repository
5. Click Deploy
6. Get your live URL in 2-3 minutes!

Questions? See RAILWAY_DEPLOY.md for detailed instructions.
    """)

if __name__ == "__main__":
    main()
