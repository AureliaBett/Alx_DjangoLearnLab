# Resolving Vercel NOT_FOUND Error - Complete Guide

## 🔍 The Error You're Facing

**Vercel Error**: `NOT_FOUND`
**Reference**: https://vercel.com/docs/errors/NOT_FOUND

This error means: **Vercel built and deployed your code, but when you made a request, it couldn't find what it was looking for.**

---

## 1️⃣ ROOT CAUSE ANALYSIS

### What Vercel Expects (vs. What You Have)

```
EXPECTED (Default Node.js App):
  ├─ index.js or vercel.json with routes pointing to valid entrypoints
  └─ Direct HTTP responses to requests

YOUR SETUP (Django Python App):
  ├─ WSGI application (social_media_api/wsgi.py)
  ├─ vercel.json pointing to wsgi.py
  ├─ Django handling all routing
  └─ Should work... but let's verify!
```

### The Problem Scenario

When you visit: `https://yourdomain.vercel.app/api/posts/`

**What SHOULD happen**:
```
1. Request hits Vercel
2. Vercel reads vercel.json
3. Sees: "route: /(.*) → dest: social_media_api/wsgi.py"
4. Invokes wsgi.py with the request
5. Django's URL routing takes over
6. Returns 200 OK with JSON
```

**What's ACTUALLY happening** (causing NOT_FOUND):
```
1. Request hits Vercel
2. Vercel can't find the entrypoint
3. OR the entrypoint isn't being invoked correctly
4. OR static files are interfering
5. Returns 404 NOT_FOUND
```

### Common Causes for Django on Vercel

| Cause | Symptom | Fix |
|-------|---------|-----|
| **Missing Python Runtime** | Build succeeds, requests fail | `@vercel/python` in vercel.json ✅ You have this |
| **Wrong WSGI Path** | Can't find wsgi.py | Path doesn't match actual location |
| **Static Files Conflict** | Some routes work, others 404 | Static files intercepting requests |
| **Missing Environment Variables** | Database connection fails | Env vars not set in Vercel |
| **Build Failures** | Silent failure during build | Check build logs in Vercel |
| **ALLOWED_HOSTS Mismatch** | Django returns 400 Bad Request | Domain not in ALLOWED_HOSTS |

---

## 2️⃣ WHY THIS ERROR EXISTS & WHAT IT PROTECTS

### The Purpose of NOT_FOUND Error

**What it's protecting you from**:
- Returning random content when no route matches
- Exposing internal server errors as silent failures
- Confusing debugging when something's actually wrong

**The Design Philosophy**:
```
Explicit > Implicit
(It's better to fail loudly and be obvious than silently return wrong data)
```

### The Request Flow in Vercel + Django

```
┌─────────────────────────────────────────────────┐
│  Browser: GET https://yourdomain.vercel.app/    │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│  Vercel Lambda Function (Python Runtime)        │
│  ├─ Reads vercel.json                           │
│  ├─ Checks routes: "/(.*)" → social_media_api   │
│  └─ Tries to invoke wsgi.py                     │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
        ┌─ YES → WSGI callable found
        │        ↓
        │     ┌──────────────────────┐
        │     │  Django gets request  │
        │     │  ├─ Checks ALLOWED_HOSTS
        │     │  ├─ Matches URL patterns
        │     │  ├─ Calls view function
        │     │  └─ Returns response
        │     └──────────────────────┘
        │
        └─ NO  → 404 NOT_FOUND ❌
```

---

## 3️⃣ DIAGNOSIS: IS YOUR CONFIG CORRECT?

### Check Your vercel.json

```json
{
  "version": 2,
  "builds": [
    {
      "src": "social_media_api/wsgi.py",    ← Must be correct path
      "use": "@vercel/python",               ← Must use Python runtime
      "config": {
        "maxLambdaSize": "15mb",
        "runtime": "python3.11"              ← Django needs Python 3.8+
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",                        ← Catch all routes
      "dest": "social_media_api/wsgi.py"    ← Send to Django
    }
  ],
  "env": {
    "DEBUG": "False",
    "ALLOWED_HOSTS": "*.vercel.app",
    "DATABASE_URL": "@database_url"         ← Must be set in Vercel
  }
}
```

### ✅ Your Config Looks Good! But...

**Potential Issues**:

1. **Environment variables not set** - Most likely culprit
2. **DATABASE_URL missing** - Causes connection errors
3. **Path issues** - If you have a different structure
4. **Build failures** - Silent failures during deployment

---

## 4️⃣ STEP-BY-STEP DIAGNOSIS & FIX

### Step 1: Check Vercel Build Logs

**In Vercel Dashboard**:
1. Go to Deployments
2. Click on your failed deployment
3. Scroll to "Build Output"
4. Look for errors like:
   - `ModuleNotFoundError: No module named 'django'`
   - `Error: /vercel/path0/social_media_api/wsgi.py not found`
   - `SyntaxError` in your code

**⚠️ THIS IS THE MOST IMPORTANT STEP**

### Step 2: Verify Environment Variables

**In Vercel Dashboard:**
1. Go to **Settings → Environment Variables**
2. Check these are set:
   ```
   DEBUG = False
   SECRET_KEY = [your-generated-key]
   ALLOWED_HOSTS = yourdomain.vercel.app
   DATABASE_URL = postgresql://...
   ```

3. Each one should have a value (not blank)

### Step 3: Test the Path

**Your project structure**:
```
social_media_api/
├── manage.py
├── social_media_api/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py        ← This is what vercel.json points to
│   └── asgi.py
├── accounts/
├── posts/
└── notifications/
```

**Your vercel.json references**:
```json
"src": "social_media_api/wsgi.py"  ← From project root, this is correct
"dest": "social_media_api/wsgi.py" ← Same path, correct
```

✅ **This matches!**

### Step 4: Check build.sh Execution

**Does your build.sh have the right order?**

```bash
#!/bin/bash
set -e

pip install -r requirements.txt        # Install packages
python manage.py collectstatic --noinput # Collect static
python manage.py migrate              # Run migrations
```

⚠️ **ISSUE FOUND**: If migrations fail, the build continues but Django is broken!

---

## 5️⃣ THE ACTUAL FIX

### Scenario A: You Haven't Deployed Yet

1. **Set Environment Variables in Vercel** (Critical!)
   ```
   Go to: Vercel → Project Settings → Environment Variables
   
   Add:
   - DEBUG = False
   - SECRET_KEY = [generate: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"]
   - ALLOWED_HOSTS = yourdomain.vercel.app
   - DATABASE_URL = [your-supabase-postgres-url]
   ```

2. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Fix: Add environment variables configuration"
   git push origin main
   ```

3. **Redeploy in Vercel**
   - Go to Deployments → Click last deployment
   - Click "Redeploy"

4. **Monitor Logs**
   - Watch the build output
   - If it says "Deployed successfully", test the API

---

### Scenario B: Deployed But Getting 404

#### Check 1: Is Database Working?

```bash
# Check if migrations ran
curl https://yourdomain.vercel.app/admin/

# If 404: Migrations didn't run
# If 500: Database connection failed
# If 200: Django is working!
```

#### Check 2: Is URL Routing Working?

```bash
# Test multiple URLs
curl https://yourdomain.vercel.app/api/posts/
curl https://yourdomain.vercel.app/accounts/register/
curl https://yourdomain.vercel.app/api/nonexistent/

# Should return:
# /api/posts/ → [] or JSON data
# /accounts/register/ → 405 Method Not Allowed (needs POST)
# /api/nonexistent/ → 404 Not Found (from Django)
```

#### Check 3: Static Files Interference?

```bash
# Check if static files are blocking routes
curl https://yourdomain.vercel.app/static/style.css
# Should return 404 (unless you have actual static files)

# This could be an issue if:
# - WhiteNoise is misconfigured
# - Static routes are too broad
```

#### Check 4: ALLOWED_HOSTS Issue?

```bash
# You'll see this in logs, but test:
curl https://yourdomain.vercel.app/api/posts/ \
  -H "Host: yourdomain.vercel.app"

# If 400 Bad Request: Check ALLOWED_HOSTS in Vercel
```

---

## 6️⃣ COMPLETE DIAGNOSTIC CHECKLIST

### Before Deploying
- [ ] `requirements.txt` has all packages: Django, gunicorn, psycopg2, dj-database-url, etc.
- [ ] `vercel.json` exists and points to `social_media_api/wsgi.py`
- [ ] `build.sh` exists and has proper permissions
- [ ] `social_media_api/wsgi.py` exists and is unchanged
- [ ] Database connection string is valid
- [ ] SECRET_KEY is generated
- [ ] ALLOWED_HOSTS includes your Vercel domain

### During Deployment
- [ ] Check Vercel build logs for errors
- [ ] Migrations should complete without errors
- [ ] `collectstatic` should complete
- [ ] No "ModuleNotFoundError" messages
- [ ] Deployment status shows "Success"

### After Deployment
- [ ] Can reach `yourdomain.vercel.app` (no 502/503)
- [ ] `/api/posts/` returns 200 OK
- [ ] `/admin/` returns 200 OK (Django admin)
- [ ] `/nonexistent/` returns 404 (Django, not Vercel)
- [ ] Database queries work (posts show up)

---

## 7️⃣ WARNING SIGNS TO WATCH FOR

### Red Flag #1: Silent Build Success
```
✅ Deployment successful
❌ But requests return 404

Problem: Build passed but runtime has issues
Solution: Check environment variables were set BEFORE deployment
```

### Red Flag #2: Mixed 200 and 404 Responses
```
✅ /api/posts/ → 200 OK
❌ /api/posts/1/ → 404 Not Found

Problem: URL routing is broken, not Vercel
Solution: Check Django urls.py configuration
```

### Red Flag #3: 502 Bad Gateway
```
❌ Error: 502 Bad Gateway
❌ Not 404, but 502

Problem: Django crashes during runtime
Solution: Check database connection, migrations
```

### Red Flag #4: Working Locally, Failing on Vercel
```
✅ python manage.py runserver → Works
❌ yourdomain.vercel.app → 404

Problem: Environment difference
Solution: Check environment variables match local .env
```

---

## 8️⃣ SIMILAR MISTAKES TO AVOID

### Mistake #1: Hardcoded Database
```python
# ❌ BAD
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydb',
        'USER': 'myuser',
        'PASSWORD': 'hardcoded-password',  # ❌ NEVER!
        'HOST': 'localhost',
    }
}

# ✅ GOOD
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL'),
        conn_max_age=600
    )
}
```

### Mistake #2: Not Handling Missing Environment Variables
```python
# ❌ BAD
SECRET_KEY = os.environ['SECRET_KEY']  # Crashes if missing!

# ✅ GOOD
SECRET_KEY = config('SECRET_KEY', default='fallback-key')
```

### Mistake #3: ALLOWED_HOSTS Too Restrictive
```python
# ❌ BAD
ALLOWED_HOSTS = ['localhost']  # Vercel domain is rejected!

# ✅ GOOD
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost', cast=Csv())
# Then in Vercel env: ALLOWED_HOSTS=yourdomain.vercel.app
```

### Mistake #4: Build Script Errors Ignored
```bash
# ❌ BAD
pip install -r requirements.txt
python manage.py collectstatic  # ← If this fails, script continues!
python manage.py migrate

# ✅ GOOD
#!/bin/bash
set -e  # ← Stop immediately if any command fails

pip install -r requirements.txt || exit 1
python manage.py collectstatic --noinput || exit 1
python manage.py migrate || exit 1
```

Your `build.sh` already has `set -e`, so you're good! ✅

---

## 9️⃣ ALTERNATIVE APPROACHES & TRADE-OFFS

### Option 1: Traditional Django on Vercel (Current)
**Pros**:
- ✅ Simple setup
- ✅ All features work
- ✅ Database migrations automatic

**Cons**:
- ❌ Cold start (2-3 seconds first request)
- ❌ Stateless functions (no persistent connections)
- ❌ Can't use WebSockets

### Option 2: Separate API + Frontend
**Pros**:
- ✅ Frontend can be on Vercel static
- ✅ API can be on Railway/Render (better for Django)
- ✅ Better separation of concerns

**Cons**:
- ❌ More complex setup
- ❌ CORS configuration needed
- ❌ Two deployments to maintain

### Option 3: Railway/Render for Django
**Pros**:
- ✅ Designed for Python
- ✅ Always-on processes
- ✅ No cold start delays

**Cons**:
- ❌ Not serverless (always running = costs)
- ❌ Overkill for small projects
- ❌ Different deployment paradigm

---

## 🔟 MENTAL MODEL: THE VERCEL REQUEST FLOW

### Understanding What Happens When You Hit a URL

```
Your URL: https://yourdomain.vercel.app/api/posts/

Step 1: DNS Resolution
  └─ yourdomain.vercel.app → Vercel IP

Step 2: Vercel Receives Request
  ├─ Reads vercel.json
  ├─ Matches route: "/(.*)" matches "/api/posts/"
  └─ Needs to run: social_media_api/wsgi.py

Step 3: Vercel Starts Python Runtime
  ├─ Loads Python 3.11 environment
  ├─ Sets environment variables
  ├─ Imports wsgi.py
  └─ Calls: application(environ, start_response)

Step 4: Django WSGI Handler
  ├─ Receives HTTP request
  ├─ Loads settings.py
  ├─ Checks ALLOWED_HOSTS ← Could fail here!
  ├─ Parses URL: /api/posts/
  └─ Matches Django URL patterns

Step 5: Django URL Router (urls.py)
  ├─ Checks: path('api/', include('posts.urls'))
  ├─ Finds: path('posts/', PostViewSet)
  ├─ Calls: posts.views.PostViewSet.list()
  └─ Returns: JSON response

Step 6: Response Back to Client
  ├─ HTTP 200 OK
  ├─ Content-Type: application/json
  └─ Body: [... posts data ...]

IF SOMETHING BREAKS AT ANY STEP:
  └─ You get either:
     - 400 Bad Request (ALLOWED_HOSTS issue)
     - 404 Not Found (URL not matched)
     - 500 Server Error (Code crashed)
     - 502 Bad Gateway (Vercel couldn't invoke wsgi.py)
```

---

## 1️⃣1️⃣ YOUR SPECIFIC FIX CHECKLIST

### Do This Now:

1. **[CRITICAL]** Add Environment Variables to Vercel
   ```
   Go to Vercel Dashboard
   → Project Name
   → Settings
   → Environment Variables
   
   Add:
   ✅ DEBUG = False
   ✅ SECRET_KEY = [generate new one]
   ✅ ALLOWED_HOSTS = yourdomain.vercel.app
   ✅ DATABASE_URL = [your supabase postgresql url]
   ✅ SUPABASE_URL = https://mpiprtcazenjurjypijw.supabase.co
   ✅ SUPABASE_KEY = eyJhbGci...
   ```

2. **[CRITICAL]** Redeploy
   ```bash
   # Option A: Push to GitHub (auto-deploys)
   git push origin main
   
   # Option B: Redeploy in Vercel Dashboard
   Click Deployments → Latest → Click "Redeploy"
   ```

3. **[IMPORTANT]** Monitor Build Logs
   - Go to Deployments
   - Click the new deployment
   - Watch the "Build" output
   - Look for errors

4. **[IMPORTANT]** Test After Deploy
   ```bash
   # Wait 2 minutes for deployment
   curl https://yourdomain.vercel.app/api/posts/
   
   # Should return:
   # [] or {"message": "..."}  ← Success!
   # 404 from Vercel           ← Still broken
   # 502 Bad Gateway           ← Database issue
   ```

---

## 1️⃣2️⃣ IF YOU'RE STILL GETTING 404

Use this decision tree:

```
Getting 404?
│
├─ Is it Vercel 404 or Django 404?
│  │
│  ├─ Check: Curl with verbose
│  │  curl -v https://yourdomain.vercel.app/api/posts/
│  │  
│  │  Look at response headers:
│  │  - "via: 1.1 varnish" → Vercel
│  │  - "Server: Werkzeug" → Django (good!)
│  │
│  └─ Vercel 404 = wsgi.py not found
│     └─ Check: vercel.json path is correct
│     └─ Check: social_media_api/wsgi.py exists locally
│     └─ Check: File is pushed to GitHub
│
├─ Django 404 (expected for invalid routes)
│  └─ Test valid routes:
│     curl https://yourdomain.vercel.app/admin/
│     curl https://yourdomain.vercel.app/api/posts/
│
└─ 502 Bad Gateway?
   ├─ DATABASE_URL not set → Set it!
   ├─ Database connection failed → Check Supabase
   ├─ Migrations failed → Check build logs
   └─ Django crash → Check settings.py
```

---

## Summary

**Your Root Cause**: Most likely **missing or incorrect environment variables** in Vercel

**Your Fix**:
1. Add all environment variables to Vercel Settings
2. Redeploy
3. Monitor build logs
4. Test with curl

**Your Prevention**:
1. Always set env vars BEFORE deploying
2. Test locally with `.env` file first
3. Check build logs for silent failures
4. Monitor first 24 hours after deploy

**Your Understanding**:
- NOT_FOUND means Vercel couldn't invoke your app
- Could also mean Django crashed during startup
- Watch for silent build successes with runtime failures

You've got this! Fix those environment variables and you'll be live. 🚀
