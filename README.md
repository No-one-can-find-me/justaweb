# Huntsman Space - Gaming Community Website

A Flask-based gaming community website with user authentication, comments system, and a modern RGB gaming theme.

## Features

- User registration and authentication
- Comment system for community interaction
- Responsive gaming-themed design
- Flash messaging system
- SQLite database for data persistence

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and navigate to `http://localhost:5000`

## Deployment on Koyeb ✅ READY

This application is **fully configured and ready** for deployment on Koyeb with automatic domain assignment.

### ✅ Pre-Deployment Checklist Complete
- [x] Flask app configured for production
- [x] Database path optimized for Koyeb ephemeral storage
- [x] Health check endpoint added (`/health`)
- [x] Gunicorn configuration optimized
- [x] Python runtime updated to 3.11.9
- [x] All dependencies specified
- [x] Error handling improved
- [x] Environment variables configured

### Quick Deployment Options

1. **Using Git Repository (Recommended):**
   ```bash
   # 1. Push to your Git repository
   git add .
   git commit -m "Ready for Koyeb deployment"
   git push origin main
   
   # 2. Go to Koyeb Dashboard
   # 3. Create App → Connect Git repository
   # 4. Koyeb auto-detects .koyeb.yml configuration
   ```

2. **Using deployment preparation script:**
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

### Deployment Configuration

**Koyeb-ready files included:**
- ✅ `.koyeb.yml` - Optimized deployment configuration
- ✅ `Procfile` - Gunicorn with production settings
- ✅ `requirements.txt` - Updated dependencies
- ✅ `runtime.txt` - Python 3.11.9
- ✅ Health check endpoint at `/health`

### App Configuration
- **Name:** mysecondweb
- **Port:** 8000
- **Instance:** nano (free tier)
- **Health Check:** `/health` endpoint
- **Database:** SQLite in `/tmp` (ephemeral)
- **Secret Key:** Pre-configured for production

### After Deployment
Your app will be available at a Koyeb domain like:
`https://mysecondweb-[random].koyeb.app`

### Important Notes
- ✅ Database automatically initializes on first request
- ✅ Optimized for Koyeb's ephemeral storage
- ✅ Production-ready error handling
- ✅ Automatic health monitoring
- ⚠️ Database resets on each deployment (use external DB for persistence)

## File Structure

```
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── Procfile           # Process file for deployment
├── runtime.txt        # Python version specification
├── .koyeb.yml         # Koyeb deployment configuration
├── static/
│   └── style.css      # CSS styles
├── templates/
│   ├── base.html      # Base template
│   ├── index.html     # Home page
│   ├── login.html     # Login page
│   ├── register.html  # Registration page
│   └── comments.html  # Comments page
└── README.md          # This file
```

## Technologies Used

- Flask (Python web framework)
- SQLite (Database)
- HTML5/CSS3
- JavaScript
- Gunicorn (WSGI server)