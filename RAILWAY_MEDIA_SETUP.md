# Railway Media Files Setup

## Important: Railway Media Files Issue

Railway's free tier **does not have persistent file storage**. This means:

- ✅ Images will upload successfully
- ❌ Images will be deleted when app restarts/redeploys
- ⚠️ Solution: Use cloud storage (AWS S3, Cloudinary, etc.)

## Current Setup (Temporary Storage)

Media files are currently stored in `/media/` folder on Railway's ephemeral file system.

### How it works:
1. User uploads image via restaurant profile
2. Image saved to `/media/restaurants/` folder
3. Image accessible at: `https://your-app.railway.app/media/restaurants/filename.jpg`
4. **Image deleted on next deployment**

## Recommended Solutions

### Option 1: Cloudinary (Free Tier - Recommended)
- Free tier: 25GB storage, 25GB bandwidth/month
- Easy Django integration
- Automatic image optimization

### Option 2: AWS S3
- Pay per use
- Most reliable
- Industry standard

### Option 3: Railway Volumes (Paid)
- Persistent storage on Railway
- Requires paid plan
- $0.25/GB/month

## For Production Use

Add this to `requirements.txt`:
```
cloudinary==1.40.0
django-cloudinary-storage==0.3.0
```

Update `settings.py` with Cloudinary config.
