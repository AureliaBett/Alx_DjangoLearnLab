# 🚀 Supabase + Vercel Deployment - Quick Start

## Your Supabase Project Ready ✅

```
Project ID: mpiprtcazenjurjypijw
URL: https://mpiprtcazenjurjypijw.supabase.co
Region: US East
Status: Active ✅
```

---

## 3-Minute Setup (Using Supabase as Your Database)

### Step 1: Get Your Connection String (1 minute)

1. Go to **https://app.supabase.com**
2. Select project **mpiprtcazenjurjypijw**
3. Click **Settings** → **Database**
4. Look for **Connection string** section
5. Select **Connection pooler** (for serverless Vercel)
6. Copy the full string

**Format**: `postgresql://postgres.[ID]:[PASSWORD]@[HOST]:6543/postgres`

### Step 2: Create .env (1 minute)

Create `.env` file in your project root:

```bash
DEBUG=False
SECRET_KEY=generate-this-yourself
ALLOWED_HOSTS=yourdomain.vercel.app
DATABASE_URL=postgresql://postgres.mpiprtcazenjurjypijw:[PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres
SUPABASE_URL=https://mpiprtcazenjurjypijw.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1waXBydGNhemVuanVyanlwaWp3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU1MDQwNTcsImV4cCI6MjA4MTA4MDA1N30.RpYEFktLkoT9RjFvwT5Ee363CfI775Otfx_AvbsFQYk
```

Replace `[PASSWORD]` with your Supabase database password.

### Step 3: Deploy (1 minute)

```bash
# Test locally first
python manage.py migrate

# Push to GitHub (auto-deploys to Vercel)
git add .
git commit -m "Add Supabase database"
git push origin main
```

**Done!** ✅

---

## What Happens on Deploy

1. ✅ Vercel reads DATABASE_URL from environment
2. ✅ Django connects to Supabase PostgreSQL
3. ✅ `build.sh` runs migrations automatically
4. ✅ Your tables are created in Supabase
5. ✅ API is live at yourdomain.vercel.app

---

## Verify Setup

### Test Locally
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
curl http://localhost:8000/api/posts/
```

### Test on Vercel
```bash
curl https://yourdomain.vercel.app/api/posts/
```

Should return: `[]` (empty array) ✅

### Check Supabase Dashboard
1. Go to https://app.supabase.com
2. Click your project
3. Go to **SQL Editor**
4. You'll see your Django tables created automatically:
   - `accounts_user`
   - `posts_post`
   - `posts_comment`
   - `posts_like`
   - `notifications_notification`

---

## Files Already Prepared

✅ `requirements.txt` - Includes Supabase packages
✅ `supabase_service.py` - Service module for Supabase client
✅ `.env.example` - Updated with Supabase fields
✅ `build.sh` - Auto-runs migrations
✅ `social_media_api/settings.py` - PostgreSQL support enabled
✅ `SUPABASE_SETUP_GUIDE.md` - Full documentation

---

## Environment Variables for Vercel

Add these to **Vercel Dashboard → Settings → Environment Variables**:

```
DATABASE_URL = postgresql://postgres.mpiprtcazenjurjypijw:[PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres

DEBUG = False

SECRET_KEY = [Generate new one]

ALLOWED_HOSTS = yourdomain.vercel.app

SUPABASE_URL = https://mpiprtcazenjurjypijw.supabase.co

SUPABASE_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1waXBydGNhemVuanVyanlwaWp3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU1MDQwNTcsImV4cCI6MjA4MTA4MDA1N30.RpYEFktLkoT9RjFvwT5Ee363CfI775Otfx_AvbsFQYk
```

---

## Common Issues

### Connection String Not Found
**Location**: Supabase → Settings → Database → Connection string
- Select "Connection pooler" (not "Direct connection")
- Copy the full PostgreSQL URL

### "Password authentication failed"
**Fix**: Replace `[PASSWORD]` with your actual Supabase database password
- Go to Supabase Settings → Database → Password reset
- Use that password in the URL

### Migrations Not Running
**Check**: 
- `build.sh` exists and includes `python manage.py migrate`
- DATABASE_URL is set in Vercel environment
- Check Vercel build logs for errors

### Tables Not Appearing
**Solution**:
- Migrations run automatically
- Wait 2-3 minutes after deployment
- Refresh Supabase dashboard
- Check Vercel logs for migration status

---

## Using Supabase Features

### Real-Time Updates
```python
from social_media_api.supabase_service import get_supabase

supabase = get_supabase()

# Listen for changes
def handle_changes(payload):
    print("Database changed:", payload)

supabase.table('posts_post').on('*', handle_changes).subscribe()
```

### File Storage (Profile Pictures)
```python
from social_media_api.supabase_service import get_supabase

supabase = get_supabase()

# Upload file
with open('profile.jpg', 'rb') as f:
    supabase.storage.from_('avatars').upload('user_123.jpg', f)

# Get public URL
url = supabase.storage.from_('avatars').get_public_url('user_123.jpg')
```

---

## Next Steps

1. ✅ Get Supabase database password
2. ✅ Create `.env` with DATABASE_URL
3. ✅ Test locally: `python manage.py migrate`
4. ✅ Add environment variables to Vercel
5. ✅ Deploy: `git push origin main`
6. ✅ Verify API is live
7. ✅ Check Supabase dashboard for tables

---

## Support

- **Supabase Setup Guide**: See `SUPABASE_SETUP_GUIDE.md`
- **Full Deployment Guide**: See `VERCEL_DEPLOYMENT_GUIDE.md`
- **Supabase Docs**: https://supabase.com/docs
- **PostgreSQL Docs**: https://www.postgresql.org/docs/

---

**Your project is ready for production!** 🚀

Deploy now and let Supabase power your database! 💪
