# Deploy ScholarSphere to Render

## 🚀 Deployment Steps

### 1. Prepare Your Render Account
1. Go to [Render.com](https://render.com/)
2. Sign up or log in with your GitHub account
3. Authorize Render to access your GitHub repositories

### 2. Create New Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `Shekhar18oct/Ai-searchEngine`
3. Grant Render permission to access the repository

### 3. Configure Web Service

**Basic Settings:**
- **Name**: `scholarsphere` (or your preferred name)
- **Region**: Choose closest to your users
- **Branch**: `main`
- **Root Directory**: Leave blank
- **Runtime**: `Python 3`

**Build & Deploy:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python src/main.py`

**Instance Type:**
- **Free** tier is sufficient for testing
- **Starter** ($7/month) for better performance

### 4. Environment Variables (Optional)
If you plan to add API keys later:
```
YOUTUBE_API_KEY=your_youtube_key
GITHUB_TOKEN=your_github_token
STACKOVERFLOW_KEY=your_stackoverflow_key
```

### 5. Deploy
1. Click **"Create Web Service"**
2. Render will automatically:
   - Clone your repository
   - Install dependencies from requirements.txt
   - Start the application
   - Provide you with a URL like: `https://scholarsphere.onrender.com`

### 6. Wait for Deployment
- Initial deployment takes 5-10 minutes
- Watch the logs for any errors
- Status will change from "Building" → "Live"

## 📝 Important Notes

### First Load May Be Slow
- Render's free tier spins down after inactivity
- First request after inactivity may take 30-50 seconds
- Subsequent requests will be fast

### Large Dependencies
Your app uses several large libraries:
- **NumPy** (~20MB)
- **SciPy** (~40MB)
- **scikit-learn** (~30MB)

Build time: ~3-5 minutes

### NLTK Data
The app automatically downloads required NLTK data on first run:
- punkt
- stopwords
- wordnet

## 🔧 Troubleshooting

### Build Fails
**Check logs for:**
1. Python version compatibility
2. Missing dependencies
3. Memory issues during scipy installation

**Solutions:**
- Verify `requirements.txt` is correct
- Check `runtime.txt` specifies Python 3.11.7
- Consider upgrading to paid tier for more build resources

### App Crashes on Start
**Common issues:**
1. Port binding - Make sure app uses `PORT` env variable
2. NLTK data download timeout
3. Memory limits exceeded

**Check:**
```python
# In src/main.py
port = int(os.getenv('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

### Slow First Search
This is normal! The first search initializes:
- NLTK lemmatizer
- Scholarly library
- API connections

Subsequent searches will be fast.

## 🌐 Post-Deployment

### Your Live URL
After deployment, you'll get: `https://your-app-name.onrender.com`

Example: `https://scholarsphere.onrender.com`

### Test Your Site
1. Visit the URL
2. Try a search: "machine learning"
3. Check all sources work:
   - Google Scholar
   - ResearchGate
   - Wikipedia

### Share Your Site
Your site is now live! Share it with:
- Students and researchers
- Academic communities
- On social media

## 📊 Monitoring

### Render Dashboard
- View deployment status
- Check logs in real-time
- Monitor resource usage
- See request metrics

### Logs
Access logs via:
1. Render Dashboard → Your Service → Logs
2. Or use Render CLI

## 🔄 Updates

### Push New Changes
```bash
git add .
git commit -m "Your update message"
git push origin main
```

Render will automatically:
- Detect the push
- Rebuild the app
- Deploy the new version

### Manual Deploy
In Render Dashboard:
- Click "Manual Deploy" → "Deploy latest commit"

## 💡 Tips

1. **Custom Domain**: Add your own domain in Render settings
2. **HTTPS**: Automatically provided by Render
3. **CDN**: Consider adding Cloudflare for faster global access
4. **Monitoring**: Set up alerts for downtime
5. **Backups**: Keep your GitHub repo updated

## 🎉 Success!

Your ScholarSphere research paper search engine is now live and accessible worldwide!

**Features:**
✅ Glass-morphism UI with animations
✅ Multi-source search (Scholar/ResearchGate/Wikipedia)
✅ Responsive design
✅ Real-time results
✅ Free hosting (with limitations)

## 📞 Support

### Issues?
1. Check Render logs
2. Review GitHub Issues
3. Update dependencies if needed
4. Contact Render support for platform issues

---

**Deployed**: Ready to share with the world! 🚀
**Repository**: https://github.com/Shekhar18oct/Ai-searchEngine
**Tech Stack**: Flask, Python, Beautiful Modern UI

Enjoy your live research paper search engine! 🎓✨
