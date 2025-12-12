# Quick Troubleshooting Guide - Vercel NOT_FOUND Error

## 🚨 You're Getting 404? Quick Fix (5 minutes)

### Step 1: Check Vercel Build Logs (2 minutes)

```
Vercel Dashboard
  → Deployments
    → Your latest deployment
      → Click "Build Output" tab
        → Look for error messages
```

**What to look for**:
```
❌ ModuleNotFoundError: No module named 'django'
   → requirements.txt missing packages
   
❌ FileNotFoundError: social_media_api/wsgi.py
   → vercel.json path is wrong
   
❌ ERROR at migration
   → DATABASE_URL not set or invalid
   
❌ ImportError in settings.py
   → Environment variable not set
```

### Step 2: Check Environment Variables (2 minutes)

```
Vercel Dashboard
  → Project Settings
    → Environment Variables
      → Make sure all 6 are present:
```

```
☑️ DEBUG = False
☑️ SECRET_KEY = [something long and random]
☑️ ALLOWED_HOSTS = yourdomain.vercel.app
☑️ DATABASE_URL = postgresql://...
☑️ SUPABASE_URL = https://mpiprtcazenjurjypijw.supabase.co
☑️ SUPABASE_KEY = eyJhbGci...
```

**If any are missing**: Add them now!

### Step 3: Redeploy (1 minute)

```bash
# Option A: Easiest
git push origin main

# Option B: Manual redeploy
# Click "Redeploy" in Vercel Deployments tab
```

### Step 4: Test (1 minute)

```bash
# Wait 2-3 minutes for deployment to complete

# Then test:
curl https://yourdomain.vercel.app/api/posts/

# Should return:
# [] or {"message": "..."}
```

---

## 📊 Error Diagnosis Table

| You See | Likely Cause | Quick Fix |
|---------|--------------|-----------|
| **Vercel 404** | wsgi.py not found | Check vercel.json path |
| **Django 404** | Invalid URL route | This is normal! Test /api/posts/ |
| **502 Bad Gateway** | Django crash | Check build logs |
| **400 Bad Request** | ALLOWED_HOSTS wrong | Add yourdomain.vercel.app to env var |
| **Connection refused** | Database offline | Check Supabase is running |
| **ModuleNotFoundError** | Missing package | Check requirements.txt |
| **Build failed** | Syntax error in code | Fix Python syntax |

---

## 🔍 Detailed Diagnostics (If Quick Fix Didn't Work)

### A. Check Vercel Build Output

```
Vercel Dashboard → Deployments → [Your Deployment] → Build Output

Look at the full log and search for:
- "ERROR"
- "FAILED"  
- "ModuleNotFoundError"
- "FileNotFoundError"
- "SyntaxError"

Copy the full error message and search:
- Google: "[error message]"
- GitHub Issues: [framework name] [error]
- StackOverflow: [error message]
```

### B. Verify Environment Variables Match vercel.json

**Your vercel.json has**:
```json
"env": {
  "DEBUG": "False",
  "ALLOWED_HOSTS": "*.vercel.app",
  "DATABASE_URL": "@database_url"
}
```

**But you also need to set in Vercel Dashboard**:
```
DEBUG = False
ALLOWED_HOSTS = yourdomain.vercel.app
DATABASE_URL = postgresql://...
SECRET_KEY = [generated]
```

⚠️ **The `@database_url` syntax in vercel.json** refers to environment variables, but they still need to be set!

### C. Check Your Actual Supabase Credentials

```bash
# In your local .env file, verify:
DATABASE_URL=postgresql://postgres.mpiprtcazenjurjypijw:[PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres

# Elements that must be correct:
# ✅ postgres.mpiprtcazenjurjypijw = Project ID
# ✅ [PASSWORD] = Your actual Supabase password
# ✅ aws-0-us-east-1.pooler = Your region
```

### D. Test Migration Locally First

```bash
# Before deploying, test locally:
python manage.py migrate

# If this fails locally, it will definitely fail on Vercel!
```

---

## ⚡ Common Causes & Fixes

### Cause #1: ALLOWED_HOSTS Empty or Wrong

```python
# In settings.py:
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost', cast=Csv())
```

**In Vercel Environment Variables, set**:
```
ALLOWED_HOSTS = yourdomain.vercel.app
```

**NOT**:
```
ALLOWED_HOSTS = *.vercel.app  ❌ Wrong format
ALLOWED_HOSTS = (empty)        ❌ Empty
```

### Cause #2: DATABASE_URL Not Set or Invalid

**In Vercel Environment Variables**:
```
DATABASE_URL = postgresql://postgres.mpiprtcazenjurjypijw:YOUR_PASSWORD@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

**Check each part**:
- `postgres.mpiprtcazenjurjypijw` = Your Supabase project ID ✅
- `YOUR_PASSWORD` = Your actual database password ✅
- `aws-0-us-east-1` = Your region ✅
- `/postgres` = Default Supabase database ✅

### Cause #3: SECRET_KEY Not Generated

```bash
# Generate a new one:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Copy the output to Vercel environment variable:
SECRET_KEY = [paste the output]
```

### Cause #4: Build Script Fails Silently

**Your build.sh**:
```bash
#!/bin/bash
set -e  # ← This stops on any error (GOOD!)

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
```

**If this fails**:
- Check Vercel build log
- Look for "ERROR" keyword
- Search for "Traceback"

### Cause #5: Requirements.txt Missing Packages

**Must have**:
```
Django==5.2.7
djangorestframework==3.14.0
gunicorn==23.0.0
psycopg2-binary==2.9.9
dj-database-url==2.1.0
whitenoise==6.6.0
python-decouple==3.8
Pillow==11.0.0
supabase>=2.0.0
python-gotrue>=2.0.0
```

**Check locally**:
```bash
pip install -r requirements.txt
python manage.py check  # Should say "System check identified no issues"
```

---

## 🧪 Testing at Each Stage

### Stage 1: Local Development
```bash
python manage.py migrate       # Should complete successfully
python manage.py runserver    # Should start without errors
curl http://localhost:8000/api/posts/  # Should return []
```

### Stage 2: Before Git Push
```bash
git status                     # Should show: On branch main
cat requirements.txt           # Should have all packages
cat vercel.json               # Should have correct paths
ls -la .env.example           # Should exist (never commit .env!)
```

### Stage 3: After Git Push
```bash
git log --oneline             # Should show your commit
# Check GitHub web: Files should be updated
```

### Stage 4: After Vercel Deploy
```bash
# Check Vercel Dashboard:
# ✅ Build Output shows "Deployed successfully"
# ✅ Deployment Preview URL works
# ✅ curl https://yourdomain.vercel.app/api/posts/
```

---

## 🆘 If You're Still Stuck

### Debug Step 1: Check Raw Vercel Response

```bash
curl -i https://yourdomain.vercel.app/api/posts/

# Check the response headers:
HTTP/1.1 404 Not Found           ← It's 404
Server: Vercel                   ← Vercel's response

# vs.

HTTP/1.1 200 OK                  ← It's 200!
Server: Werkzeug                 ← Django's response
Content-Type: application/json

# vs.

HTTP/1.1 502 Bad Gateway         ← Django crashed
```

### Debug Step 2: Check Admin Page

```bash
curl https://yourdomain.vercel.app/admin/

# If this returns:
# - 200 OK → Django is running, URL routing broken
# - 404 → Django WSGI not being invoked
# - 502 → Django crash during startup
```

### Debug Step 3: Check Vercel Function Logs

```
Vercel Dashboard → Your Project → Functions
→ See if there are any error logs showing runtime issues
```

### Debug Step 4: Rebuild with --force

```
Vercel Dashboard → Deployments → [latest]
→ Click "Redeploy"
→ Uncheck "Use existing cache"
→ Click "Redeploy"
```

---

## 📝 Pre-Deployment Checklist

Before you push to Vercel:

```
CODE
  ☐ No syntax errors: python -m py_compile social_media_api/*.py
  ☐ All imports work: python manage.py check
  ☐ Migrations work locally: python manage.py migrate

CONFIGURATION
  ☐ requirements.txt has all packages
  ☐ vercel.json points to social_media_api/wsgi.py
  ☐ build.sh has set -e
  ☐ .env.example has all field names
  ☐ .gitignore includes .env

ENVIRONMENT
  ☐ Supabase project created and active
  ☐ Database password obtained
  ☐ DATABASE_URL format correct
  ☐ SECRET_KEY generated

GIT
  ☐ All changes committed
  ☐ Pushed to origin main
  ☐ GitHub shows latest files

VERCEL
  ☐ Project linked to GitHub
  ☐ All 6 environment variables set:
     ☐ DEBUG = False
     ☐ SECRET_KEY = [generated]
     ☐ ALLOWED_HOSTS = yourdomain.vercel.app
     ☐ DATABASE_URL = postgresql://...
     ☐ SUPABASE_URL = https://...
     ☐ SUPABASE_KEY = eyJhbGci...
```

If all checkboxes are checked, deployment should succeed! ✅

---

## 🎯 Most Common Reason for NOT_FOUND

**95% of the time**: Environment variables not set in Vercel before deployment

**The fix**:
1. Set all 6 environment variables in Vercel Dashboard
2. Redeploy
3. Wait 3 minutes
4. Test API

That's it! 🚀

---

## Reference Documentation

- **Full Guide**: `NOT_FOUND_ERROR_FIX.md`
- **Vercel Docs**: https://vercel.com/docs/errors/NOT_FOUND
- **Django Deployment**: https://docs.djangoproject.com/en/5.2/howto/deployment/
- **Supabase Setup**: `SUPABASE_QUICK_START.md`

Good luck! You've got this! 💪
