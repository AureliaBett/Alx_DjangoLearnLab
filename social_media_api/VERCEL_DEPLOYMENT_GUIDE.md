# Social Media API - Vercel Deployment Guide

## Project Overview

This is a Django REST Framework API for a social media application with the following features:

### Key Components:
- **Accounts App**: User registration, login, profiles, follow/unfollow functionality
- **Posts App**: CRUD operations for posts, comments, and likes with proper permissions
- **Notifications App**: Real-time notifications for user interactions

### Technology Stack:
- Django 5.2.7 with Django REST Framework
- PostgreSQL (production) / SQLite (development)
- Token-based authentication
- Custom user model

---

## Prerequisites

Before deploying to Vercel, you need:

1. **Vercel Account** - Sign up at [vercel.com](https://vercel.com)
2. **Git Repository** - Push your code to GitHub, GitLab, or Bitbucket
3. **PostgreSQL Database** - Set up a hosted PostgreSQL instance (e.g., Railway, Supabase, Render, or AWS RDS)
4. **Python 3.11+** installed locally

---

## Step 1: Prepare Your Local Environment

### 1.1 Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 1.2 Install dependencies
```bash
pip install -r requirements.txt
```

### 1.3 Create a `.env` file locally
```bash
DEBUG=True
SECRET_KEY=your-local-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3  # For local development
```

### 1.4 Run migrations locally
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### 1.5 Test locally
```bash
python manage.py runserver
```

---

## Step 2: Set Up PostgreSQL Database

### Option A: Using Railway (Recommended for Beginners)
1. Go to [railway.app](https://railway.app)
2. Sign up and create a new project
3. Add PostgreSQL plugin
4. Copy the `DATABASE_URL` from the plugin settings
5. Format: `postgresql://user:password@host:port/dbname`

### Option B: Using Supabase
1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Go to Settings > Database
4. Copy the PostgreSQL connection string
5. Format: `postgresql://postgres:[password]@[host]:[port]/postgres`

### Option C: Using Render
1. Go to [render.com](https://render.com)
2. Create a PostgreSQL database
3. Copy the internal connection string
4. Will look like: `postgresql://...`

---

## Step 3: Prepare Code for Vercel

All necessary files have been created:

✅ `requirements.txt` - Python dependencies
✅ `vercel.json` - Vercel configuration
✅ `.vercelignore` - Files to exclude from deployment
✅ `build.sh` - Build script for migrations
✅ `social_media_api/settings.py` - Updated with environment variables

### Key Changes Made:

1. **Added Environment Variable Support**:
   - `SECRET_KEY` - Read from environment
   - `DEBUG` - Controlled by environment
   - `ALLOWED_HOSTS` - Configurable per deployment
   - `DATABASE_URL` - PostgreSQL support

2. **Updated Security Settings**:
   - SSL redirect only in production
   - WhiteNoise for static files serving
   - Proper CORS configuration

3. **Database Configuration**:
   - Automatic PostgreSQL detection
   - Falls back to SQLite for development

---

## Step 4: Push Code to GitHub

```bash
git init
git add .
git commit -m "Prepare Django app for Vercel deployment"
git branch -M main
git remote add origin https://github.com/your-username/your-repo.git
git push -u origin main
```

---

## Step 5: Deploy to Vercel

### 5.1 Via Vercel CLI (Recommended)
```bash
npm i -g vercel  # Install Vercel CLI globally
vercel           # Deploy your project
```

### 5.2 Via Vercel Dashboard
1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import your GitHub repository
4. Select the repository
5. Vercel will detect Django settings automatically
6. Proceed to next step

### 5.3 Configure Environment Variables in Vercel

In your Vercel project settings, add these environment variables:

| Variable | Value | Notes |
|----------|-------|-------|
| `DEBUG` | `False` | Production setting |
| `SECRET_KEY` | Generate a strong secret | Use `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `ALLOWED_HOSTS` | `yourdomain.vercel.app` | Add your custom domain if you have one |
| `DATABASE_URL` | Your PostgreSQL connection string | From Railway/Supabase/Render |
| `SECURE_SSL_REDIRECT` | `True` | Force HTTPS |

**To add environment variables in Vercel:**
1. Go to your project's Settings
2. Navigate to Environment Variables
3. Add each variable
4. Redeploy the project

---

## Step 6: Troubleshooting

### Issue 1: Database Migration Failures
**Solution**: The `build.sh` script runs migrations automatically. If you need to manually migrate:
```bash
vercel env pull  # Pull environment variables
python manage.py migrate
```

### Issue 2: Static Files Not Loading
**Verification**: WhiteNoise is configured in `settings.py` and `requirements.txt` includes it.
```bash
python manage.py collectstatic --noinput
```

### Issue 3: ALLOWED_HOSTS Error
**Solution**: Update the environment variable in Vercel to include your domain:
```
yourdomain.vercel.app,www.yourdomain.vercel.app
```

### Issue 4: 502 Bad Gateway
**Debugging**:
1. Check Vercel Function logs: `vercel logs`
2. Verify DATABASE_URL is correct
3. Ensure migrations ran successfully
4. Check SECRET_KEY is set

### Issue 5: Media Files Upload
For production, configure AWS S3:
1. Update `requirements.txt` to include `boto3==1.28.0` and `django-storages==1.14.2`
2. Add AWS credentials to environment variables
3. Update `settings.py` with S3 configuration

---

## Step 7: Custom Domain (Optional)

1. In Vercel dashboard, go to Settings > Domains
2. Add your custom domain (e.g., `api.example.com`)
3. Update DNS records as shown by Vercel
4. Update `ALLOWED_HOSTS` in environment variables

---

## Step 8: Monitor and Maintain

### View Logs
```bash
vercel logs
```

### Check Deployments
Go to your Vercel dashboard and monitor deployments in real-time.

### Database Backups
- Railway/Supabase: Automatic daily backups
- Remember to enable backups in your database provider

---

## API Endpoints

Once deployed, your API will be available at:

```
https://yourdomain.vercel.app/api/posts/
https://yourdomain.vercel.app/accounts/register/
https://yourdomain.vercel.app/accounts/login/
```

Test your deployment:
```bash
curl https://yourdomain.vercel.app/api/posts/
```

---

## Key Features Deployed

✅ **User Authentication**: Token-based auth via `/accounts/login/`
✅ **Posts Management**: Full CRUD at `/api/posts/`
✅ **Comments & Likes**: Nested resources for engagement
✅ **Follow System**: User relationships with notifications
✅ **Notifications**: Real-time updates on user interactions
✅ **Permissions**: Role-based access control
✅ **Static Files**: Served via WhiteNoise

---

## Environment Variables Reference

```
# Django
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.vercel.app

# Database
DATABASE_URL=postgresql://user:password@host:port/dbname

# CORS (if frontend is separate)
CORS_ALLOWED_ORIGINS=https://yourdomain.com

# AWS S3 (optional, for media)
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_STORAGE_BUCKET_NAME=your-bucket
```

---

## Security Best Practices

1. ✅ Never commit `.env` files
2. ✅ Use strong SECRET_KEY (generate with Django)
3. ✅ Enable SSL redirect in production
4. ✅ Set secure cookies
5. ✅ Use HSTS headers
6. ✅ Keep dependencies updated: `pip install --upgrade -r requirements.txt`
7. ✅ Regularly backup your PostgreSQL database

---

## Performance Tips

1. **Database Indexing**: Add database indexes for frequently queried fields
2. **Caching**: Consider implementing Redis for caching
3. **Pagination**: API already supports pagination via DRF
4. **Connection Pooling**: PostgreSQL connection pooling is configured in `settings.py`

---

## Support & Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework Docs](https://www.django-rest-framework.org/)
- [Vercel Python Deployment](https://vercel.com/docs/concepts/functions/serverless-functions)
- [Railway PostgreSQL](https://docs.railway.app/)

---

## Next Steps

1. Set up your PostgreSQL database
2. Generate a secure SECRET_KEY
3. Configure environment variables in Vercel
4. Deploy using `vercel` CLI or dashboard
5. Test your API endpoints
6. Monitor logs and set up alerts
7. Implement frontend and CORS settings if needed

Congratulations! Your Django API is now ready for production deployment! 🚀
