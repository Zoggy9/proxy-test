# Deploying Web Proxy to Render

Complete step-by-step guide to deploy your web proxy on Render's free tier.

## Prerequisites

- GitHub account (free)
- Render account (free) - sign up at https://render.com

## Step-by-Step Deployment Guide

### Step 1: Create a GitHub Repository

1. Go to https://github.com and sign in
2. Click the **"+"** button (top right) → **"New repository"**
3. Name it something like `web-proxy` or `my-proxy-server`
4. Choose **Public** (required for Render free tier)
5. Click **"Create repository"**

### Step 2: Upload Your Files to GitHub

**Option A: Using GitHub Web Interface (Easiest)**

1. On your new repository page, click **"uploading an existing file"**
2. Drag and drop these files:
   - `proxy_server.py`
   - `requirements.txt`
   - `render.yaml`
   - `README.md`
3. Click **"Commit changes"**

**Option B: Using Git Command Line**

```bash
# In the folder with your proxy files
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/web-proxy.git
git push -u origin main
```

### Step 3: Deploy on Render

1. Go to https://render.com and sign in
2. Click **"New +"** button → **"Web Service"**
3. Click **"Connect account"** to connect your GitHub
4. Find your `web-proxy` repository and click **"Connect"**

### Step 4: Configure Your Service

Render will auto-detect the settings from `render.yaml`, but verify:

- **Name:** `web-proxy` (or your choice)
- **Environment:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn proxy_server:app`
- **Plan:** Select **"Free"**

Click **"Create Web Service"**

### Step 5: Wait for Deployment

- Render will start building your app (takes 2-5 minutes)
- Watch the logs - you'll see it installing dependencies
- When you see "Your service is live 🎉", it's ready!

### Step 6: Access Your Proxy

- Render will give you a URL like: `https://web-proxy-xxxx.onrender.com`
- Click on it or copy it to your browser
- Your proxy is now live on the internet! 🚀

## Important Notes

### Free Tier Limitations

⚠️ **Render's free tier:**
- Your app will "spin down" after 15 minutes of inactivity
- First request after inactivity takes 30-60 seconds to wake up
- 750 hours/month of runtime (enough for personal use)
- No credit card required

### Security & Usage

⚠️ **Remember:**
- This is for **educational purposes only**
- Don't share your proxy URL publicly (could be abused)
- Some websites may block proxy access
- Your free tier has bandwidth limits

### Custom Domain (Optional)

Want a custom domain like `myproxy.com`?
1. Go to your service settings on Render
2. Click "Custom Domain"
3. Follow instructions to add your domain

## Troubleshooting

### Build Failed?

Check the logs in Render dashboard:
- Look for errors in red
- Common issue: Make sure `requirements.txt` includes all dependencies

### App Won't Start?

1. Check the logs for error messages
2. Make sure `gunicorn` is in `requirements.txt`
3. Verify `render.yaml` is in your repository root

### "Service Unavailable" Error?

- Your app might be spinning down (free tier)
- Wait 30-60 seconds and refresh
- The first request wakes it up

### Site Won't Load Through Proxy?

Some sites block proxies - try simpler websites first like:
- http://example.com
- http://info.cern.ch
- https://httpbin.org

## Updating Your Proxy

Made changes to your code?

1. Update files on GitHub (upload new versions)
2. Render will automatically detect changes
3. It will rebuild and redeploy (takes 2-5 minutes)

Or use git:
```bash
git add .
git commit -m "Updated proxy"
git push
```

Render auto-deploys on every push to `main` branch!

## Monitoring Your App

In Render dashboard you can:
- View live logs
- See deployment history
- Monitor bandwidth usage
- Check uptime
- View environment variables

## Next Steps

### Improve Your Proxy:

1. **Add authentication** - Prevent unauthorized use
2. **Add request logging** - See what's being accessed
3. **Improve error handling** - Better user messages
4. **Add caching** - Speed up repeat visits
5. **Custom styling** - Make it your own

### Example: Add Basic Auth

```python
from flask import request, Response
from functools import wraps

def check_auth(username, password):
    return username == 'admin' and password == 'yourpassword'

def authenticate():
    return Response('Login required', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/', methods=['GET', 'POST'])
@requires_auth  # Add this decorator
def proxy():
    # ... rest of your code
```

## Costs

- **Free tier:** $0/month (perfect for learning)
- **Starter:** $7/month (no spin down, better for production)

For learning and personal use, the free tier is perfect!

## Support

- Render Documentation: https://render.com/docs
- Render Community: https://community.render.com
- Check your Render dashboard logs for issues

## Files Explained

**render.yaml** - Tells Render how to build and run your app
**requirements.txt** - Lists Python packages needed
**proxy_server.py** - Your main application code
**README.md** - Documentation

---

🎉 **Congratulations!** You now have a live web proxy on the internet!

Share the URL with friends (but be careful - set up auth if you do!)
