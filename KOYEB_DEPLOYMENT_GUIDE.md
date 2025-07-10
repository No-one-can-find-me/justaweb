# Koyeb Deployment Guide - Free Starter Plan

This Flask web application is optimized for deployment on Koyeb's free starter plan.

## Project Overview

**Huntsman Space** is a Flask web application with user authentication and commenting system featuring:
- User registration and login
- Comment posting system
- SQLite database (ephemeral storage)
- Responsive web design
- Health check endpoint for monitoring

## Deployment Configuration

### Files Optimized for Koyeb Free Plan:

1. **`.koyeb.yml`** - Main deployment configuration
2. **`Procfile`** - Process definition for gunicorn
3. **`requirements.txt`** - Python dependencies
4. **`runtime.txt`** - Python version specification
5. **`app.py`** - Main Flask application with optimizations

### Key Optimizations for Free Plan:

- **Instance Type**: `nano` (free tier compatible)
- **Workers**: 1 gunicorn worker (memory efficient)
- **Database**: SQLite in `/tmp` (ephemeral, suitable for free tier)
- **Health Check**: Optimized with proper timeouts
- **Resource Management**: Memory and CPU optimized settings
- **Security**: Production-ready session configuration

## Deployment Steps

### 1. Prerequisites
- Git repository (GitHub, GitLab, etc.)
- Koyeb account (free)

### 2. Repository Setup
```bash
# Initialize git if not already done
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit for Koyeb deployment"

# Push to your remote repository
git push origin main
```

### 3. Koyeb Deployment

#### Option A: Using Koyeb Dashboard
1. Log in to [Koyeb Dashboard](https://app.koyeb.com)
2. Click "Create App"
3. Select "GitHub" or your git provider
4. Choose your repository
5. Koyeb will automatically detect the `.koyeb.yml` configuration
6. Click "Deploy"

#### Option B: Using Koyeb CLI
```bash
# Install Koyeb CLI
npm install -g @koyeb/cli

# Login to Koyeb
koyeb login

# Deploy from current directory
koyeb app deploy justaweb
```

### 4. Environment Variables (Already Configured)
The following environment variables are pre-configured in `.koyeb.yml`:
- `SECRET_KEY`: Flask secret key for sessions
- `PORT`: Application port (8000)
- `DATABASE_PATH`: SQLite database path (/tmp/database.db)
- `FLASK_ENV`: Production environment

## Application Features

### Routes Available:
- `/` - Home page with recent comments
- `/login` - User login
- `/register` - User registration
- `/logout` - User logout
- `/comments` - Comments page
- `/health` - Health check endpoint

### Database Schema:
- **users**: id, username, password, created_at
- **comments**: id, username, text, timestamp

## Important Notes for Free Plan

### Limitations:
1. **Ephemeral Storage**: Database resets on each deployment
2. **Sleep Mode**: App may sleep after inactivity
3. **Resource Limits**: Limited CPU and memory
4. **Single Instance**: Only 1 instance allowed

### Recommendations:
1. **Data Persistence**: For production, consider upgrading to paid plan with persistent storage
2. **Monitoring**: Use the `/health` endpoint for uptime monitoring
3. **Performance**: App is optimized for free tier resource constraints

## Troubleshooting

### Common Issues:

1. **App Won't Start**
   - Check logs in Koyeb dashboard
   - Verify all required files are present
   - Ensure Python version compatibility

2. **Database Errors**
   - Database is ephemeral and resets on deployment
   - Check `/health` endpoint for database connectivity

3. **Port Issues**
   - App is configured for port 8000
   - Koyeb automatically handles port mapping

### Health Check
Monitor your app health at: `https://your-app-url.koyeb.app/health`

Expected response:
```json
{
  "status": "healthy",
  "message": "Application is running",
  "database": "connected"
}
```

## File Structure
```
justaweb/
├── .koyeb.yml              # Koyeb deployment config
├── app.py                  # Main Flask application
├── Procfile               # Process definition
├── requirements.txt       # Python dependencies
├── runtime.txt           # Python version
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── comments.html
├── static/              # CSS and static files
│   └── style.css
└── README.md           # This file
```

## Support

For Koyeb-specific issues:
- [Koyeb Documentation](https://www.koyeb.com/docs)
- [Koyeb Community](https://community.koyeb.com)

For application issues:
- Check application logs in Koyeb dashboard
- Verify health check endpoint
- Review Flask application logs

---

**Ready to deploy!** 🚀

Your Flask application is now optimized and ready for deployment on Koyeb's free starter plan.