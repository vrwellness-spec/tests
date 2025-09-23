# Render Deployment Guide

## Overview
This guide will help you deploy your Assessment Application to Render, a modern cloud platform that offers free hosting for web applications.

## Prerequisites
- GitHub account (to connect your repository)
- Render account (free at render.com)
- Your project code pushed to a GitHub repository

## Step 1: Prepare Your Repository

### 1.1 Push to GitHub
Make sure all your project files are committed and pushed to a GitHub repository:

```bash
git init
git add .
git commit -m "Initial commit - Assessment Application"
git branch -M main
git remote add origin https://github.com/yourusername/your-repo-name.git
git push -u origin main
```

### 1.2 Verify Required Files
Ensure these files are in your repository root:
- ✅ `render.yaml` - Render configuration
- ✅ `requirements.txt` - Python dependencies
- ✅ `wsgi.py` - WSGI entry point
- ✅ `app.py` - Main Flask application
- ✅ `config.py` - Configuration with environment variables
- ✅ All templates and static files

## Step 2: Deploy to Render

### 2.1 Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account
3. Authorize Render to access your repositories

### 2.2 Create New Web Service
1. **Click "New +"** in Render dashboard
2. **Select "Web Service"**
3. **Connect your GitHub repository**
4. **Configure the service:**
   - **Name:** `assessment-app` (or your preferred name)
   - **Environment:** `Python`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn --bind 0.0.0.0:$PORT wsgi:application`

### 2.3 Configure Environment Variables
Render will automatically read from `render.yaml`, but you can also set manually:

**Required Variables:**
- `ADMIN_USERNAME` - Your admin username
- `ADMIN_PASSWORD` - Secure admin password
- `SECRET_KEY` - Flask secret key (generate a random string)
- `FLASK_DEBUG` - Set to `False`
- `DATABASE_PATH` - `/opt/render/project/src/assessments.db`

**Optional Variables:**
- `MAIL_SERVER` - Email server for notifications
- `MAIL_PORT` - Email port (587 for TLS)
- `MAIL_USE_TLS` - `True`
- `MAIL_USERNAME` - Your email
- `MAIL_PASSWORD` - Email password/app password

### 2.4 Configure Persistent Disk (Important!)
1. In your service settings, go to **"Disks"**
2. **Add a disk:**
   - **Name:** `assessment-data`
   - **Mount Path:** `/opt/render/project/src`
   - **Size:** `1 GB` (free tier)

This ensures your SQLite database persists between deployments.

## Step 3: Deploy and Test

### 3.1 Deploy
1. **Click "Create Web Service"**
2. **Wait for deployment** (usually 2-5 minutes)
3. **Monitor build logs** for any errors

### 3.2 Access Your Application
Once deployed, you'll get a URL like:
`https://your-app-name.onrender.com`

### 3.3 Test Functionality
1. **Visit your application URL**
2. **Test login** with your admin credentials
3. **Create a test assessment**
4. **Verify all features work:**
   - Assessment creation/editing
   - Student assessment taking
   - Results viewing
   - PDF/Word generation
   - Static files loading

## Step 4: Automatic Deployments

### 4.1 Enable Auto-Deploy
Render automatically deploys when you push to your main branch:
1. Make changes to your code
2. Commit and push to GitHub
3. Render automatically rebuilds and deploys

### 4.2 Manual Deploy
You can also trigger manual deployments:
1. Go to your service in Render dashboard
2. Click **"Manual Deploy"**
3. Select **"Deploy latest commit"**

## Troubleshooting

### Common Issues

**1. Build Failures**
- Check `requirements.txt` for correct package versions
- Ensure `gunicorn` is included in requirements.txt
- Verify Python version compatibility
- Review build logs in Render dashboard

**2. Application Won't Start**
- Check `wsgi.py` configuration
- Verify all imports work correctly
- Check start command: `python wsgi.py`

### Common Issues and Solutions

1. **ModuleNotFoundError: No module named 'your_application'**
   - **Cause:** Incorrect WSGI application reference in gunicorn command
   - **Solution:** Ensure the start command uses `gunicorn --bind 0.0.0.0:$PORT wsgi:application`
   - **Note:** The format is `module_name:variable_name` where `wsgi` is the file and `application` is the Flask app variable

2. **Build fails with "gunicorn: command not found"**
   - **Cause:** `gunicorn` is not installed
   - **Solution:** Ensure `gunicorn` is included in your `requirements.txt` file

**3. Database Issues**
- Ensure persistent disk is configured
- Check `DATABASE_PATH` environment variable
- Verify write permissions

**4. Static Files Not Loading**
- Check Flask static file configuration
- Verify file paths in templates
- Ensure static files are in repository

**5. Environment Variables**
- Check all required variables are set
- Verify variable names match config.py
- Use Render dashboard to update variables

### Getting Help

1. **Check Render Logs:**
   - Go to your service dashboard
   - Click on "Logs" tab
   - Review recent application logs

2. **Render Documentation:**
   - Visit [render.com/docs](https://render.com/docs)
   - Check Python deployment guides

3. **Community Support:**
   - Render Community Forum
   - GitHub Issues (if using open source)

## Production Considerations

### Security
- ✅ Use strong admin passwords
- ✅ Set secure SECRET_KEY
- ✅ Disable debug mode
- ✅ Use environment variables for sensitive data

### Performance
- Monitor application performance in Render dashboard
- Consider upgrading to paid plan for better performance
- Optimize database queries if needed

### Backups
- **Database:** Download SQLite file regularly
- **Code:** Keep GitHub repository updated
- **Environment Variables:** Document all settings

### Monitoring
- Use Render's built-in monitoring
- Set up alerts for downtime
- Monitor application logs regularly

## Render.yaml Configuration

Your `render.yaml` file automates the deployment:

```yaml
services:
  - type: web
    name: assessment-app
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: python wsgi.py
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: FLASK_DEBUG
        value: False
    disk:
      name: assessment-data
      mountPath: /opt/render/project/src
      sizeGB: 1
```

## Free Tier Limitations

Render's free tier includes:
- ✅ 750 hours/month (enough for continuous hosting)
- ✅ Automatic SSL certificates
- ✅ Custom domains
- ❌ Sleeps after 15 minutes of inactivity
- ❌ Limited to 512MB RAM
- ❌ 1GB persistent disk

**Note:** Free services "sleep" after 15 minutes of inactivity and take 30+ seconds to wake up.

## Upgrading to Paid Plan

For production use, consider upgrading:
- **Starter Plan:** $7/month - No sleeping, more resources
- **Standard Plan:** $25/month - Enhanced performance
- **Pro Plan:** $85/month - High performance, priority support

---

Your Assessment Application is now ready for deployment to Render! 🚀