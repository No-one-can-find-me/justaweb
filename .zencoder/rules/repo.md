---
description: Repository Information Overview
alwaysApply: true
---

# Huntsman Space - Gaming Website Information

## Summary
Huntsman Space is a professional dark-themed gaming website built with Flask, featuring a Discord-like chat system and modern UI for gamers. It includes user authentication, real-time messaging, social media integration, and responsive design that works on both desktop and mobile devices.

## Structure
- **app.py**: Main Flask application entry point
- **templates/**: HTML templates using Jinja2 templating engine
- **static/**: CSS, JavaScript, and image assets
- **datas/**: Text files for storing user data and chat messages
- **.vscode/**: VS Code configuration
- **railway.json & render.yaml**: Deployment configuration files

## Language & Runtime
**Language**: Python
**Version**: Python 3.11.0 (specified in render.yaml)
**Framework**: Flask 2.3.3
**WSGI Server**: Gunicorn 21.2.0
**Template Engine**: Jinja2 3.1.2

## Dependencies
**Main Dependencies**:
- Flask==2.3.3
- Werkzeug==2.3.7
- Jinja2==3.1.2
- MarkupSafe==2.1.3
- itsdangerous==2.1.2
- click==8.1.7
- gunicorn==21.2.0

## Build & Installation
```bash
# Clone the repository
git clone <repo-url>
cd justaweb

# Install dependencies
pip install -r requirements.txt

# Run the application locally
python app.py
```

## Deployment
**Railway Deployment**:
- Uses NIXPACKS builder
- Start command: `gunicorn app:app`
- Health check path: `/`
- Restart policy: ON_FAILURE (max 10 retries)

**Render Deployment**:
- Web service type
- Python environment
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`
- Python version: 3.11.0
- Environment variables:
  - SECRET_KEY (auto-generated)
  - FLASK_ENV=production

## Main Files & Resources
**Entry Point**: app.py
**Templates**:
- base.html: Base template with common elements
- index.html: Home page
- login.html & register.html: Authentication pages
- chat.html: Real-time chat interface
- profile.html: User profile page with editable fields

**Static Assets**:
- CSS: style.css (custom dark theme with gaming aesthetics)
- JavaScript: script.js (handles real-time chat functionality)
- Images: Profile icons and other visual elements

**Data Storage**:
- datas/users.txt: JSON file storing user credentials
- datas/chats.txt: JSON file storing chat messages

## Features
- User authentication system with session management
- Real-time chat with message polling
- Active user tracking
- Rate limiting for message sending
- Admin user functionality
- User profile management (edit name, username, and bio)
- Responsive design with custom CSS
- Flash message notification system
- Social media integration
- YouTube video embedding