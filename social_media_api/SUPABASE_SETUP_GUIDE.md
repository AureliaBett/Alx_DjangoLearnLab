# Supabase Integration Guide for Django

## Your Supabase Credentials

```
Project URL: https://mpiprtcazenjurjypijw.supabase.co
Anon Key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1waXBydGNhemVuanVyanlwaWp3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU1MDQwNTcsImV4cCI6MjA4MTA4MDA1N30.RpYEFktLkoT9RjFvwT5Ee363CfI775Otfx_AvbsFQYk
```

---

## Option 1: Using Supabase as PostgreSQL Database (Recommended)

This is the **best approach** for your Django app - use Supabase's PostgreSQL directly via Django ORM.

### Step 1: Get PostgreSQL Connection String

1. Go to [https://app.supabase.com](https://app.supabase.com)
2. Select your project
3. Click **Settings** (bottom left)
4. Click **Database** in the submenu
5. Scroll to **Connection string**
6. Select **Connection pooler** (recommended for serverless)
7. Copy the connection string starting with `postgresql://`

**Format**:
```
postgresql://postgres.[PROJECT_ID]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
```

Replace:
- `[PASSWORD]` - Your Supabase database password (from Settings > Database > Password reset)
- `[PROJECT_ID]` - Your project reference ID (mpiprtcazenjurjypijw)
- `[REGION]` - Your region

### Step 2: Update .env File

```bash
DEBUG=False
SECRET_KEY=your-generated-secret-key
ALLOWED_HOSTS=yourdomain.vercel.app,localhost
DATABASE_URL=postgresql://postgres.[PROJECT_ID]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
```

### Step 3: Install Connection Pooling Package

```bash
pip install dj-database-url
```

Your `requirements.txt` already has this, so you're good!

### Step 4: Run Migrations

Locally first:
```bash
python manage.py migrate
```

Then on Vercel (automatic via build.sh):
- Migrations run automatically during deployment
- Your Supabase database will be initialized

---

## Option 2: Using Supabase Python Client Library

If you want to use Supabase SDK alongside Django:

### Step 1: Install Supabase Package

```bash
pip install supabase python-gotrue
```

### Step 2: Add to requirements.txt

```
supabase>=2.0.0
python-gotrue>=2.0.0
```

### Step 3: Create a Supabase Service

Create `social_media_api/supabase_service.py`:

```python
import os
from supabase import create_client, Client

class SupabaseService:
    _instance: Client = None
    
    @classmethod
    def get_client(cls) -> Client:
        if cls._instance is None:
            url = os.environ.get("SUPABASE_URL")
            key = os.environ.get("SUPABASE_KEY")
            
            if not url or not key:
                raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set")
            
            cls._instance = create_client(url, key)
        
        return cls._instance

# Usage
supabase = SupabaseService.get_client()
```

### Step 4: Add Credentials to .env

```bash
SUPABASE_URL=https://mpiprtcazenjurjypijw.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1waXBydGNhemVuanVyanlwaWp3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU1MDQwNTcsImV4cCI6MjA4MTA4MDA1N30.RpYEFktLkoT9RjFvwT5Ee363CfI775Otfx_AvbsFQYk
```

---

## For Django: Use PostgreSQL Connection (Recommended)

Since your Django app uses Django ORM, **use Option 1** (PostgreSQL connection string).

### Your DATABASE_URL Should Be:

```
postgresql://postgres.mpiprtcazenjurjypijw:[YOUR_PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

Replace `[YOUR_PASSWORD]` with your actual Supabase database password.

### settings.py Already Supports This:

```python
if config('DATABASE_URL', default=None):
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=config('DATABASE_URL'),
            conn_max_age=600
        )
    }
```

Just add DATABASE_URL to your environment variables! ✅

---

## Step-by-Step Setup with Your Supabase

### 1. Get Your Database Password

Go to [https://app.supabase.com](https://app.supabase.com):
1. Select your project
2. Settings → Database → Password reset
3. Copy your password (you'll use it in the connection string)

### 2. Build Your Connection String

Format:
```
postgresql://postgres.mpiprtcazenjurjypijw:YOUR_PASSWORD@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

**Example** (NOT real):
```
postgresql://postgres.mpiprtcazenjurjypijw:pWn_12345678901234567890@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

### 3. Test Connection Locally

```bash
# Install PostgreSQL client (Windows)
choco install postgresql  # or download pgAdmin

# Test connection
psql "postgresql://postgres.mpiprtcazenjurjypijw:YOUR_PASSWORD@aws-0-us-east-1.pooler.supabase.com:6543/postgres"
```

### 4. Add to .env

```bash
DATABASE_URL=postgresql://postgres.mpiprtcazenjurjypijw:YOUR_PASSWORD@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

### 5. Run Migrations Locally

```bash
python manage.py migrate
```

This will create all your tables in Supabase PostgreSQL!

### 6. Deploy to Vercel

1. Go to Vercel dashboard
2. Select your project
3. Settings → Environment Variables
4. Add:
   ```
   DATABASE_URL=postgresql://postgres.mpiprtcazenjurjypijw:YOUR_PASSWORD@aws-0-us-east-1.pooler.supabase.com:6543/postgres
   ```
5. Redeploy: Click "Redeploy" or push to GitHub

---

## Supabase Features You Can Use

### 1. Real-time Subscriptions
Subscribe to database changes:

```python
from social_media_api.supabase_service import supabase

# Listen to posts table
response = supabase.table('posts_post').on('*', lambda payload: print(payload)).subscribe()
```

### 2. File Storage
Store profile pictures in Supabase Storage:

```python
from social_media_api.supabase_service import supabase

# Upload file
with open('profile.jpg', 'rb') as f:
    supabase.storage.from_('avatars').upload('user_123/profile.jpg', f)

# Get public URL
url = supabase.storage.from_('avatars').get_public_url('user_123/profile.jpg')
```

### 3. Authentication
Supabase Auth can work alongside Django Auth:

```python
from social_media_api.supabase_service import supabase

# Sign up
response = supabase.auth.sign_up({
    "email": "user@example.com",
    "password": "password"
})

# Sign in
response = supabase.auth.sign_in_with_password({
    "email": "user@example.com",
    "password": "password"
})
```

---

## Common Issues & Solutions

### Issue: Connection Refused
**Solution**: Check your password is correct and connection string matches your region.

### Issue: SSL Certificate Error
**Solution**: Add `?sslmode=require` to your DATABASE_URL:
```
postgresql://postgres.mpiprtcazenjurjypijw:PASSWORD@aws-0-us-east-1.pooler.supabase.com:6543/postgres?sslmode=require
```

### Issue: Connection Pool Timeout
**Solution**: Settings.py already has `conn_max_age=600`. This is good.

### Issue: Migrations Not Running
**Solution**: Check build.sh includes `python manage.py migrate` - it does! ✅

---

## Supabase Dashboard

After deployment, check your database:

1. Go to [https://app.supabase.com](https://app.supabase.com)
2. Select your project
3. Click **SQL Editor** or **Table Editor**
4. You'll see your Django tables:
   - `accounts_user`
   - `posts_post`
   - `posts_comment`
   - `posts_like`
   - `notifications_notification`

---

## Your Complete Setup

```
✅ Supabase Project: mpiprtcazenjurjypijw
✅ Database Type: PostgreSQL
✅ Connection Method: Connection Pooler (Recommended)
✅ Django ORM: Fully compatible
✅ Django Migrations: Auto-runs
✅ Storage: Available for media files
```

---

## Environment Variables for Vercel

Add these to Vercel Settings → Environment Variables:

```
DEBUG=False
SECRET_KEY=[Your generated key]
ALLOWED_HOSTS=yourdomain.vercel.app
DATABASE_URL=postgresql://postgres.mpiprtcazenjurjypijw:PASSWORD@aws-0-us-east-1.pooler.supabase.com:6543/postgres
SUPABASE_URL=https://mpiprtcazenjurjypijw.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1waXBydGNhemVuanVyanlwaWp3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU1MDQwNTcsImV4cCI6MjA4MTA4MDA1N30.RpYEFktLkoT9RjFvwT5Ee363CfI775Otfx_AvbsFQYk
```

---

## Quick Deploy Checklist

- [ ] Get Supabase database password
- [ ] Build DATABASE_URL connection string
- [ ] Test connection locally: `python manage.py migrate`
- [ ] Add DATABASE_URL to Vercel environment
- [ ] Deploy: `git push origin main` or `vercel --prod`
- [ ] Verify in Supabase dashboard that tables exist
- [ ] Test API: `curl https://yourdomain.vercel.app/api/posts/`

---

## Support

- Supabase Docs: https://supabase.com/docs
- PostgreSQL Docs: https://www.postgresql.org/docs/
- Django Database: https://docs.djangoproject.com/en/5.2/ref/settings/#databases

**Your Supabase integration is ready!** 🚀
