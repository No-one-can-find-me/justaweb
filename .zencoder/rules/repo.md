---
description: Repository Information Overview
alwaysApply: true
---

# Huntsman Space - Gaming Website Information

## Summary
Huntsman Space is a professional dark-themed gaming website built with Flask, featuring modern UI for gamers. It includes user authentication, social media integration, and responsive design that works on both desktop and mobile devices.

## Structure
- **app.py**: Main Flask application entry point
- **templates/**: HTML templates using Jinja2 templating engine
- **static/**: CSS, JavaScript, and image assets
- **datas/**: Text files for storing user data
- **Procfile**: Deployment configuration for hosting platforms
- **railway.json**: Railway-specific deployment configuration
- **render.yaml**: Render-specific deployment configuration

## Language & Runtime
**Language**: Python
**Version**: Python 3.11.0 (specified in render.yaml)
**Framework**: Flask 2.3.3
**WSGI Server**: Gunicorn 21.2.0
**Template Engine**: Jinja2 3.1.2

## Dependencies
**Main Dependencies**:
- Flask==2.3.3: Web framework
- Werkzeug==2.3.7: WSGI utility library
- Jinja2==3.1.2: Template engine
- MarkupSafe==2.1.3: String handling for HTML
- itsdangerous==2.1.2: Security helpers
- click==8.1.7: Command line interface
- gunicorn==21.2.0: WSGI HTTP server

## Build & Installation
```bash
# Clone the repository
git clone <repo-url>
cd justaweb

# Install dependencies
pip install -r requirements.txt

# Run the application locally
python app.py

# Access the application at http://localhost:8080
```

## Deployment
**Platforms**:
- Railway: Configured with railway.json and Procfile
- Render: Configured with render.yaml

**Railway Configuration**:
- Uses NIXPACKS builder
- Start command: `gunicorn app:app`
- Health check path: `/`
- Restart policy: ON_FAILURE (max 10 retries)

**Render Configuration**:
- Web service type
- Python environment (version 3.11.0)
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`
- Environment variables:
  - SECRET_KEY (auto-generated)
  - FLASK_ENV=production

## Main Files & Resources
**Entry Point**: app.py
**Templates**:
- base.html: Base template with common elements
- index.html: Home page with welcome message and features
- login.html/register.html: User authentication pages
- profile.html: User profile management
- shop.html: Virtual shop interface
- minigames.html: Gaming features

**Data Storage**:
- datas/users.txt: JSON file storing user credentials and profiles
- datas/redeem_codes.txt: Stores redemption codes
- datas/shop_items.txt: Stores shop items

## Features
- User authentication with enhanced validation
- Profile management (display name, bio)
- Virtual currency system with shop and redemption codes
- Admin user functionality
- Responsive design with custom CSS animations
- Flash message notification system
- Social media integration (YouTube, Kick, Discord)
- YouTube video embedding