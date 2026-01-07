# Render Deployment Guide for ScholarSphere

## Prerequisites
- GitHub account with your code pushed
- Render account (free tier available)

## Deployment Steps

### 1. Prepare Your Repository
Make sure these files are in your repository:
- `requirements.txt` - All Python dependencies
- `Procfile` - Tells Render how to run your app
- `runtime.txt` - Specifies Python version
- `render.yaml` - Render service configuration

### 2. Sign Up / Log In to Render
- Go to [render.com](https://render.com)
- Sign up or log in with GitHub

### 3. Create New Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Select your `Ai-searchEngine` repository

### 4. Configure Build Settings
- **Name**: `scholarsphere` (or your preferred name)
- **Runtime**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python src/main.py`

### 5. Environment Variables (Optional)
Add any API keys or environment variables if needed:
- `PYTHON_VERSION`: 3.11.6
- `PORT`: 5000

### 6. Deploy
- Click **"Create Web Service"**
- Render will automatically build and deploy your app
- You'll get a URL like: `https://scholarsphere.onrender.com`

## Troubleshooting

### Build Fails
- Check that `requirements.txt` has all dependencies
- Verify Python version compatibility (3.11.6)
- Review build logs in Render dashboard

### App Crashes on Start
- Check `src/main.py` runs without errors locally
- Verify Flask is configured to use `0.0.0.0` host
- Check start logs in Render dashboard

### Slow Performance
- Free tier has limited resources
- Consider upgrading to paid tier for better performance
- Google Scholar searches may be slow (expected behavior)

## Important Notes

⚠️ **Free Tier Limitations**:
- App goes to sleep after 15 minutes of inactivity
- First request after sleep will be slow (30-60 seconds)
- Limited to 512 MB RAM

✅ **Recommended Settings**:
- Use Python 3.11.6 (not 3.13 - has compatibility issues)
- Keep dependencies minimal
- Monitor build logs for errors

## Alternative Deployment Options

If Render doesn't work:
- **PythonAnywhere**: Free tier, easy Flask deployment
- **Heroku**: Free tier available (requires credit card)
- **Vercel**: Supports Python serverless functions
- **Railway**: Similar to Render with free tier

## Support

For issues:
1. Check Render build logs
2. Test locally first: `python src/main.py`
3. Verify all dependencies install: `pip install -r requirements.txt`
4. Check Flask runs on port 5000
