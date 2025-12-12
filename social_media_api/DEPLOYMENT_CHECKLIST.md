# Vercel Deployment Checklist

## Pre-Deployment ✓

- [ ] **Code pushed to GitHub**
  ```bash
  git push origin main
  ```

- [ ] **Python 3.11+ installed locally**
  ```bash
  python --version
  ```

- [ ] **requirements.txt verified**
  - All dependencies listed
  - No conflicting versions
  - Check: `pip freeze > requirements-check.txt`

- [ ] **.env.example created** (never commit actual .env)
  - Contains all required variables
  - Documented with examples

- [ ] **build.sh is executable**
  ```bash
  chmod +x build.sh
  ```

---

## Database Setup ✓

Choose ONE: Railway | Supabase | Render | AWS RDS

- [ ] **PostgreSQL database created**
- [ ] **DATABASE_URL copied** (looks like: `postgresql://user:pass@host:port/db`)
- [ ] **Test connection locally** (optional but recommended)
  ```bash
  psql $DATABASE_URL
  ```

---

## Vercel Setup ✓

- [ ] **Vercel account created** at [vercel.com](https://vercel.com)
- [ ] **GitHub repository connected**
- [ ] **Project created on Vercel** (auto-imported from GitHub)
- [ ] **Python runtime detected** (Vercel auto-detects from vercel.json)

---

## Environment Variables ✓

Set these in Vercel Dashboard → Project Settings → Environment Variables:

### Required Variables
```
□ DEBUG = False
□ SECRET_KEY = [generate new]
□ ALLOWED_HOSTS = yourdomain.vercel.app
□ DATABASE_URL = [from Step 2]
```

**To generate SECRET_KEY**:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Optional Variables
```
□ CORS_ALLOWED_ORIGINS = https://yourdomain.com
□ SENTRY_DSN = [if using Sentry for error tracking]
□ LOG_LEVEL = INFO
```

---

## First Deployment ✓

- [ ] **Trigger deployment**
  - Option A: Push to GitHub (auto-deploys)
  - Option B: Use Vercel CLI: `vercel --prod`

- [ ] **Monitor build logs**
  ```bash
  vercel logs --follow
  ```

- [ ] **Wait for deployment to complete** (usually 2-3 mins)

---

## Post-Deployment Verification ✓

- [ ] **Test API is live**
  ```bash
  curl https://yourdomain.vercel.app/api/posts/
  # Should return: []  or  {"detail": ...}
  ```

- [ ] **Check no 502 Bad Gateway errors**
  - If 502: Check DATABASE_URL in Vercel
  - If still error: Check Vercel logs

- [ ] **Verify database migrations ran**
  - Should complete in build.sh
  - Check: View in Vercel build output

- [ ] **Test a POST endpoint** (requires token, but should not 500)
  ```bash
  curl -X POST https://yourdomain.vercel.app/accounts/register/ \
    -H "Content-Type: application/json" \
    -d '{"username":"test","email":"test@example.com","password":"pass123"}'
  ```

---

## Troubleshooting Guide ✓

### 502 Bad Gateway
```
Cause: Database connection issue
Fix: 
  1. Verify DATABASE_URL in Vercel environment
  2. Check PostgreSQL is running
  3. Redeploy: vercel --prod
```

### DisallowedHost Error
```
Cause: Domain not in ALLOWED_HOSTS
Fix:
  1. Go to Vercel Dashboard → Settings → Environment Variables
  2. Update ALLOWED_HOSTS = yourdomain.vercel.app
  3. Redeploy
```

### Module Not Found
```
Cause: Dependency missing from requirements.txt
Fix:
  1. pip install missing_package
  2. pip freeze > requirements.txt
  3. Push to GitHub, auto-redeploys
```

### Static Files Not Loading
```
Cause: WhiteNoise not configured
Fix: Already configured! Check settings.py has:
  - STATICFILES_STORAGE = 'whitenoise.storage...'
  - MIDDLEWARE includes 'whitenoise.middleware...'
  - Redeploy with: vercel --prod --force
```

### Migrations Not Running
```
Cause: build.sh not executed
Fix:
  1. Check build.sh is executable: chmod +x build.sh
  2. Verify in vercel.json: "builds" includes correct reference
  3. Redeploy and check logs
```

---

## Security Checklist ✓

- [ ] **SECRET_KEY is strong** (not default, 50+ chars)
- [ ] **DEBUG is False** in production
- [ ] **Database URL is from environment** (not hardcoded)
- [ ] **HTTPS redirect enabled** (automatic on Vercel)
- [ ] **SECURE_SSL_REDIRECT = True** (in settings.py)
- [ ] **SECURE_HSTS_SECONDS set** to high value
- [ ] **No credentials in version control** (.env in .gitignore)
- [ ] **PostgreSQL password is strong**

---

## Performance Checklist ✓

- [ ] **Static files minified** (WhiteNoise handles this)
- [ ] **Database indexes created** (recommendations in CODEBASE_ANALYSIS.md)
- [ ] **Pagination enabled** (DRF default)
- [ ] **Query optimization** (consider N+1 fixes)
- [ ] **Caching strategy planned** (optional, for later)

---

## Monitoring Setup ✓

- [ ] **Vercel logs accessible**
  ```bash
  vercel logs  # View recent logs
  vercel logs --follow  # Real-time logs
  ```

- [ ] **Error tracking setup** (optional)
  - Recommended: Sentry (free tier available)
  - Add SENTRY_DSN to environment variables

- [ ] **Database monitoring enabled**
  - Railway: Built-in dashboard
  - Supabase: Built-in analytics
  - AWS: CloudWatch

---

## Custom Domain (Optional) ✓

- [ ] **Domain registered** (namecheap, godaddy, etc.)
- [ ] **In Vercel: Settings → Domains → Add Domain**
- [ ] **DNS records updated** (Vercel shows instructions)
- [ ] **Wait 24 hours for DNS propagation**
- [ ] **Update ALLOWED_HOSTS environment variable**
  ```
  ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,yourdomain.vercel.app
  ```
- [ ] **Redeploy after DNS propagates**

---

## Frontend Integration (If Applicable) ✓

- [ ] **CORS enabled** (add to INSTALLED_APPS if needed)
- [ ] **Frontend .env configured** with API URL
- [ ] **Token storage strategy decided** (localStorage/cookie)
- [ ] **API calls updated** to use new domain
- [ ] **Test requests from frontend** to API

---

## Backup & Recovery ✓

- [ ] **Database backups enabled**
  - Railway: Automatic daily
  - Supabase: Automatic daily
  - AWS: Configure manually

- [ ] **Recovery procedure documented**
  - How to restore from backup
  - How to export data
  - How to migrate to new database

- [ ] **Code backup (GitHub)**
  - Repository tags for major releases
  - `git tag -a v1.0.0 -m "Production release"`

---

## Documentation ✓

- [ ] **README.md includes deployment instructions**
- [ ] **Environment variables documented** (.env.example)
- [ ] **API documentation available** (Swagger/OpenAPI planned)
- [ ] **Database schema documented** (in CODEBASE_ANALYSIS.md)
- [ ] **Team has access** to Vercel/Database dashboards

---

## Success Indicators ✓

Your deployment is successful when:

```
✅ API endpoint responds with 200 OK
✅ No 502 Bad Gateway errors
✅ Database queries work
✅ Authentication tokens can be generated
✅ Posts can be created/read/updated/deleted
✅ HTTPS is enforced
✅ Static files load quickly
✅ No error logs with status 500
```

---

## Next Steps

1. **Monitor for 24 hours** - Check logs regularly
2. **Load test** - See how API performs under load
3. **Set up alerts** - Get notified of errors
4. **Plan scaling** - If traffic increases
5. **Regular backups** - Configure automatic backup strategy

---

## Rollback Procedure

If something goes wrong:

**Option 1: Revert Code**
```bash
git revert HEAD
git push origin main
# Vercel auto-redeploys with previous version
```

**Option 2: Restore Database**
- Use your database provider's restore function
- Railway/Supabase: One-click restore in dashboard

**Option 3: Revert Environment Variables**
- Vercel keeps history of env variable changes
- Revert to previous values in Dashboard

---

## Contact & Support

- Vercel Status: https://www.vercel-status.com
- Django Docs: https://docs.djangoproject.com
- DRF Docs: https://www.django-rest-framework.org
- Railroad/Supabase: Check their status pages

---

**Date Deployed**: ___________
**Deployed By**: ___________
**Production URL**: ___________
**Notes**: ___________________________________________

---

Good luck! 🚀 Your API is ready for the world!
