# Railway Database Persistence Guide

## ⚠️ **CRITICAL: Why Data Gets Deleted on Railway**

Railway free tier has specific behaviors that can cause data loss:

### **Common Causes:**

1. **Database Service Restart**
   - Free tier databases can be paused/restarted
   - Data persists IF using Railway's PostgreSQL plugin
   - Data LOST if using ephemeral storage

2. **Deployment Triggers**
   - Every git push triggers new deployment
   - Migrations run on each deployment
   - If migrations have `--flush` flag, data is deleted

3. **Service Recreation**
   - Deleting and recreating Railway services
   - Changing database plugin
   - Switching between staging/production

## ✅ **Solutions Implemented:**

### **1. Proper Railway Database Setup**
```bash
# Railway Dashboard:
# 1. Add PostgreSQL Plugin (NOT ephemeral storage)
# 2. Link to your service
# 3. DATABASE_URL automatically set
```

### **2. Safe Migration Command**
```bash
# railway.json & Procfile use:
python manage.py migrate --noinput

# NEVER use:
python manage.py migrate --run-syncdb  # Recreates tables
python manage.py flush  # Deletes all data
```

### **3. Database Connection Settings**
```python
# settings.py now has:
DATABASES = {
    'default': {
        'conn_max_age': 600,  # Reuse connections
        'conn_health_checks': True,  # Verify before using
        'ATOMIC_REQUESTS': True,  # Transaction safety
    }
}
```

### **4. Data Backup Strategy**
```bash
# Backup script (run manually):
python backup_database.py

# Restore script (after data loss):
python restore_database.py
```

## 🔍 **How to Check Database Status:**

### **Option A: Railway Dashboard**
```
1. Go to Railway project
2. Click PostgreSQL service
3. Click "Data" tab
4. View tables and data
```

### **Option B: Railway CLI**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Connect to database
railway run python check_railway_db.py

# Or direct psql access
railway connect
```

### **Option C: Django Shell**
```bash
railway run python manage.py shell

# Then in shell:
from django.contrib.auth.models import User
User.objects.count()  # Should return user count
```

## 🚨 **Data Loss Prevention Checklist:**

- [ ] ✅ Using Railway PostgreSQL Plugin (not ephemeral)
- [ ] ✅ DATABASE_URL environment variable set
- [ ] ✅ Migrations use `--noinput` only
- [ ] ✅ No `flush` or `--run-syncdb` commands
- [ ] ✅ Regular database backups taken
- [ ] ✅ Connection pooling configured
- [ ] ✅ Atomic transactions enabled

## 📊 **Check Your Setup:**

Run this locally to verify Railway connection:
```bash
# Set Railway DATABASE_URL
$env:DATABASE_URL = "postgresql://user:pass@host:port/db"

# Check connection
python check_railway_db.py
```

## 🔧 **If Data Gets Deleted Again:**

1. **Check Railway Logs:**
   ```
   Railway Dashboard → Deployments → View Logs
   Look for: "Applying migrations" or "Database reset"
   ```

2. **Verify PostgreSQL Service:**
   ```
   Railway Dashboard → PostgreSQL → Metrics
   Check: Uptime, Storage Used, Connections
   ```

3. **Restore from Backup:**
   ```bash
   railway run python restore_database.py
   ```

4. **Manual Data Entry:**
   ```bash
   railway run python create_test_user.py
   railway run python create_admin.py
   ```

## 🎯 **Railway Free Tier Limitations:**

| Feature | Free Tier | Impact |
|---------|-----------|--------|
| **Database Size** | 512MB | Should be enough for testing |
| **Uptime** | Can pause | Inactive apps may pause |
| **Persistence** | ✅ YES | Data should persist with PostgreSQL plugin |
| **Backups** | Manual | You must backup yourself |

## 💡 **Best Practices:**

1. **Always use Railway's PostgreSQL plugin**
2. **Never delete the PostgreSQL service**
3. **Take regular backups before deployments**
4. **Test migrations locally first**
5. **Monitor Railway dashboard for issues**
6. **Keep backup files in Git** (database_backup/ folder)

## 🆘 **Emergency Recovery:**

If all data is lost:
```bash
# 1. Verify database exists
railway variables

# 2. Run migrations
railway run python manage.py migrate

# 3. Restore backup
railway run python restore_database.py

# 4. Create admin
railway run python create_admin.py

# 5. Verify
railway run python check_railway_db.py
```
