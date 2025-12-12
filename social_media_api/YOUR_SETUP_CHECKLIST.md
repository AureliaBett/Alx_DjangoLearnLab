# Your Django + Supabase Setup - Complete Checklist

## Your Credentials (Saved for Reference)

```
Project ID:  mpiprtcazenjurjypijw
Project URL: https://mpiprtcazenjurjypijw.supabase.co
Anon Key:    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1waXBydGNhemVuanVyanlwaWp3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU1MDQwNTcsImV4cCI6MjA4MTA4MDA1N30.RpYEFktLkoT9RjFvwT5Ee363CfI775Otfx_AvbsFQYk
```

**⚠️ IMPORTANT**: Keep these safe and never commit to GitHub!

---

## Step 1: Get Your Database Password (5 minutes)

### 1.1 Access Supabase Dashboard
- Go to: https://app.supabase.com
- Sign in with your account
- Click on project **mpiprtcazenjurjypijw**

### 1.2 Reset Database Password
1. Click **Settings** (bottom left sidebar)
2. Click **Database** in the submenu
3. Scroll down to **Password** section
4. Click **Reset password**
5. Copy the new password displayed
6. **Save this somewhere safe** (you'll need it multiple times)

### 1.3 Get Connection String
1. In same **Settings → Database** page
2. Look for **Connection string** section
3. Click the dropdown showing **Connection pooler**
4. Copy the entire connection string
5. It looks like:
   ```
   postgresql://postgres.mpiprtcazenjurjypijw:[PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres
   ```

---

## Step 2: Create Your .env File (3 minutes)

### 2.1 In Your Project Root, Create `.env`

**Windows PowerShell**:
```powershell
New-Item -Path ".env" -Type File
```

**macOS/Linux**:
```bash
touch .env
```

### 2.2 Add This Content to `.env`

```bash
# Django Settings
DEBUG=True
SECRET_KEY=django-insecure-dev-key-for-local-testing
ALLOWED_HOSTS=localhost,127.0.0.1

# Supabase Database
DATABASE_URL=postgresql://postgres.mpiprtcazenjurjypijw:[YOUR_PASSWORD_HERE]@aws-0-us-east-1.pooler.supabase.com:6543/postgres

# Supabase Client (Optional)
SUPABASE_URL=https://mpiprtcazenjurjypijw.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1waXBydGNhemVuanVyanlwaWp3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU1MDQwNTcsImV4cCI6MjA4MTA4MDA1N30.RpYEFktLkoT9RjFvwT5Ee363CfI775Otfx_AvbsFQYk
```

⚠️ **Replace `[YOUR_PASSWORD_HERE]` with the password you got in Step 1.2**

### 2.3 Verify .env is in .gitignore

```bash
# Check if .gitignore exists
cat .gitignore

# If you see .env in the list, you're good!
# If not, add it:
echo ".env" >> .gitignore
```

---

## Step 3: Test Locally (5 minutes)

### 3.1 Install/Update Requirements
```bash
pip install -r requirements.txt
```

### 3.2 Run Migrations
```bash
python manage.py migrate
```

**Expected output**:
```
Operations to perform:
  Apply all migrations: accounts, admin, auth, contenttypes, posts, sessions, notifications
Running migrations:
  ... (list of migrations)
  ✓ All migrations applied successfully
```

### 3.3 Create a Superuser (Optional)
```bash
python manage.py createsuperuser
```

Follow prompts to create admin user.

### 3.4 Test the API Locally
```bash
python manage.py runserver
```

**In another terminal**:
```bash
curl http://localhost:8000/api/posts/
```

**Expected response**:
```json
[]
```

**Success!** ✅

---

## Step 4: Verify in Supabase Dashboard (2 minutes)

### 4.1 Check Tables Were Created
1. Go to https://app.supabase.com
2. Select project **mpiprtcazenjurjypijw**
3. Click **SQL Editor** (left sidebar)
4. You should see these tables:
   - `accounts_user`
   - `posts_post`
   - `posts_comment`
   - `posts_like`
   - `notifications_notification`

### 4.2 Verify Data
1. Click on **Table Editor** (left sidebar)
2. Select `accounts_user`
3. You should see your superuser if you created one

**Everything working?** ✅ Continue to Step 5!

---

## Step 5: Prepare for Production (3 minutes)

### 5.1 Generate a Secure SECRET_KEY
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Copy the output** - you'll use this for Vercel.

### 5.2 Update .env for Production
```bash
DEBUG=False
SECRET_KEY=[PASTE_THE_GENERATED_KEY_HERE]
ALLOWED_HOSTS=yourdomain.vercel.app,localhost,127.0.0.1
DATABASE_URL=postgresql://postgres.mpiprtcazenjurjypijw:[YOUR_PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres
SUPABASE_URL=https://mpiprtcazenjurjypijw.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1waXBydGNhemVuanVyanlwaWp3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU1MDQwNTcsImV4cCI6MjA4MTA4MDA1N30.RpYEFktLkoT9RjFvwT5Ee363CfI775Otfx_AvbsFQYk
```

### 5.3 Push to GitHub
```bash
git add .
git commit -m "Add Supabase integration and database setup"
git push origin main
```

---

## Step 6: Deploy to Vercel (5 minutes)

### 6.1 Go to Vercel Dashboard
1. https://vercel.com/dashboard
2. Select your project (or import if new)

### 6.2 Add Environment Variables
**Settings → Environment Variables** - Add these 6 variables:

| Variable | Value |
|----------|-------|
| `DEBUG` | `False` |
| `SECRET_KEY` | [Your generated key] |
| `ALLOWED_HOSTS` | `yourdomain.vercel.app` |
| `DATABASE_URL` | `postgresql://postgres.mpiprtcazenjurjypijw:[PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres` |
| `SUPABASE_URL` | `https://mpiprtcazenjurjypijw.supabase.co` |
| `SUPABASE_KEY` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` |

### 6.3 Redeploy
1. Click **Deployments** tab
2. Click **Redeploy** on latest deployment
3. Or push to GitHub (auto-redeploys)

**Wait 2-3 minutes for deployment...**

---

## Step 7: Test on Vercel (2 minutes)

### 7.1 Get Your Vercel URL
**Vercel Dashboard** → **Deployments** → **Copy URL**

Example: `https://your-project.vercel.app`

### 7.2 Test the API
```bash
curl https://your-project.vercel.app/api/posts/
```

**Expected response**:
```json
[]
```

### 7.3 Test Registration
```bash
curl -X POST https://your-project.vercel.app/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPassword123!"
  }'
```

**Success?** ✅ Your API is live!

---

## Step 8: Custom Domain (Optional, 10 minutes)

### 8.1 Add Domain to Vercel
1. **Vercel Dashboard → Settings → Domains**
2. Click **Add Domain**
3. Enter your domain (e.g., `api.yourdomain.com`)
4. Follow Vercel's DNS instructions

### 8.2 Update Environment Variables
Add your custom domain to `ALLOWED_HOSTS`:
```
ALLOWED_HOSTS=yourdomain.vercel.app,api.yourdomain.com
```

### 8.3 Redeploy
Push to GitHub or click Redeploy in Vercel.

---

## Complete Checklist

### Local Setup
- [ ] Password from Supabase (Step 1.2)
- [ ] Database connection string (Step 1.3)
- [ ] `.env` file created with credentials (Step 2)
- [ ] `.gitignore` includes `.env` (Step 2.3)
- [ ] `pip install -r requirements.txt` (Step 3.1)
- [ ] `python manage.py migrate` successful (Step 3.2)
- [ ] `python manage.py runserver` works (Step 3.4)
- [ ] Tables visible in Supabase (Step 4.1)

### Production Setup
- [ ] Generated SECRET_KEY (Step 5.1)
- [ ] Updated `.env` for production (Step 5.2)
- [ ] Pushed to GitHub (Step 5.3)
- [ ] Added 6 environment variables to Vercel (Step 6.2)
- [ ] Redeployed on Vercel (Step 6.3)
- [ ] API responds at Vercel URL (Step 7.2)
- [ ] Registration works (Step 7.3)

### Optional
- [ ] Set up custom domain (Step 8)
- [ ] Monitor in Supabase dashboard
- [ ] Monitor in Vercel dashboard
- [ ] Set up error tracking (Sentry)

---

## Common Commands

```bash
# Check environment
python manage.py shell
>>> import os
>>> print(os.environ.get('DATABASE_URL'))

# View migrations
python manage.py showmigrations

# Create new migrations
python manage.py makemigrations

# Run specific migration
python manage.py migrate accounts

# Database shell (if psql installed)
psql $DATABASE_URL

# Clear cache
python manage.py clear_cache

# Django admin
python manage.py createsuperuser
```

---

## Troubleshooting

### ❌ "Could not connect to database"
**Check**:
- PASSWORD is correct in DATABASE_URL
- URL format matches: `postgresql://postgres.mpiprtcazenjurjypijw:[PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres`
- Connection string is from "Connection pooler" (not "Direct connection")

### ❌ "Module not found: supabase"
**Fix**: `pip install -r requirements.txt`

### ❌ "Migrations not running"
**Check**:
- `build.sh` exists
- `DATABASE_URL` set in Vercel
- Check Vercel build logs for errors

### ❌ "Tables not appearing"
**Solution**:
- Wait 3-5 minutes after deployment
- Run `python manage.py migrate` locally first
- Check Vercel logs for migration output
- Refresh Supabase dashboard

---

## What Happens on Vercel

1. ✅ Code deployed
2. ✅ Environment variables loaded
3. ✅ `build.sh` runs
   - Installs dependencies
   - Runs `python manage.py migrate`
   - Collects static files
4. ✅ Django app starts
5. ✅ Connected to Supabase PostgreSQL
6. ✅ API is live!

---

## Next Steps

1. **Complete this checklist**
2. **Verify everything works locally** (Step 3-4)
3. **Deploy to Vercel** (Step 6)
4. **Test on production** (Step 7)
5. **Monitor and enjoy!** 🎉

---

## Resources

- **Supabase Docs**: https://supabase.com/docs
- **Django Docs**: https://docs.djangoproject.com/
- **Vercel Docs**: https://vercel.com/docs
- **Your Setup Guide**: `SUPABASE_SETUP_GUIDE.md`
- **Full Deployment**: `VERCEL_DEPLOYMENT_GUIDE.md`

---

## Support

Having issues? Check these files:
- `SUPABASE_QUICK_START.md` - Quick reference
- `SUPABASE_SETUP_GUIDE.md` - Detailed setup
- `DEPLOYMENT_CHECKLIST.md` - General deployment help
- `VERCEL_DEPLOYMENT_GUIDE.md` - Full guide

**Your API is ready!** 🚀 Deploy now and celebrate! 🎉
