# Quick Start: Deploy to Vercel in 10 Minutes

## TL;DR - Fast Deployment Path

### Step 1: Prepare Database (2 mins)
Choose ONE option:

**Option A - Railway (Easiest)**:
1. Visit [railway.app](https://railway.app)
2. Sign in with GitHub
3. Create new project → Add PostgreSQL
4. Copy the `DATABASE_URL` from settings

**Option B - Supabase**:
1. Visit [supabase.com](https://supabase.com)
2. New project → Copy `postgresql://...` connection string

### Step 2: Push to GitHub (2 mins)
```bash
git add .
git commit -m "Deploy to Vercel"
git push origin main
```

### Step 3: Deploy on Vercel (3 mins)
```bash
npm i -g vercel
vercel
```

When prompted, answer:
- Set up and deploy? → **Y**
- Which scope? → Your name
- Link to existing project? → **N**
- Project name? → `social-media-api`
- Framework? → Django
- Root directory? → `./` (current)

### Step 4: Set Environment Variables (3 mins)
Go to Vercel Dashboard → Your Project → Settings → Environment Variables

Add these:
```
DEBUG=False
SECRET_KEY=[Generate: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"]
ALLOWED_HOSTS=yourdomain.vercel.app
DATABASE_URL=[Your PostgreSQL URL from Step 1]
```

### Step 5: Redeploy (0 mins)
Vercel auto-redeploys when you add env vars. Done! 🚀

---

## Test Your Deployment

```bash
# Replace with your Vercel domain
curl https://yourdomain.vercel.app/api/posts/

# Expected response:
# []  (empty array - no posts yet)
```

---

## Common Issues & Fixes

| Error | Fix |
|-------|-----|
| `502 Bad Gateway` | Check DATABASE_URL in environment variables |
| `ModuleNotFoundError` | All dependencies are in requirements.txt |
| `DisallowedHost` | Update ALLOWED_HOSTS env var with your domain |
| `ProgrammingError` | Migrations run in build.sh automatically |

---

## What's Been Set Up

✅ `requirements.txt` - All Python packages
✅ `vercel.json` - Vercel configuration  
✅ `build.sh` - Auto migrations on deploy
✅ `settings.py` - Environment variables support
✅ Static files - WhiteNoise configured
✅ Database - PostgreSQL ready

---

## Next: Integrate with Frontend

Add this to your frontend `.env`:
```
REACT_APP_API_URL=https://yourdomain.vercel.app
```

Then make API calls:
```javascript
const response = await fetch(
  `${process.env.REACT_APP_API_URL}/api/posts/`
);
```

---

## Database Backups

If using Railway or Supabase, automatic backups are enabled. Check their dashboards for backup settings.

---

## Custom Domain (Optional)

1. In Vercel: Settings → Domains → Add Domain
2. Update DNS records (Vercel shows instructions)
3. Update `ALLOWED_HOSTS` environment variable
4. Redeploy

---

## Support

- 📖 Full guide: `VERCEL_DEPLOYMENT_GUIDE.md`
- 📊 Architecture: `CODEBASE_ANALYSIS.md`
- 💬 Issues? Check Vercel logs: `vercel logs`

---

You're done! Your Django API is live on Vercel! 🎉
