# Railway CLI Installation and Usage Guide

## Install Railway CLI (Windows PowerShell)
# Run this in PowerShell:
npm install -g @railway/cli

# Or use Scoop:
scoop install railway

## Login to Railway
railway login

## Link to your project
railway link

## Run migrations on Railway
railway run python manage.py migrate

## Create superuser on Railway
railway run python manage.py createsuperuser

## Restore database backup
railway run python restore_database.py

## Check deployment logs
railway logs

## Open Railway dashboard
railway open
