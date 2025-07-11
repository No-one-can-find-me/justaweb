# Huntsman Space - Gaming Website

A professional dark-themed gaming website built with Flask, featuring a modern UI perfect for gamers.

## Features

- **Dark Professional Gaming Theme**: Custom CSS with neon accents and smooth animations
- **Responsive Design**: Works perfectly on desktop and mobile devices
- **User Authentication**: Login/Register system with session management
- **Comment System**: Interactive community comments with real-time posting
- **Social Media Integration**: Links to YouTube, Kick, and Discord
- **Video Integration**: Embedded YouTube video in the About section
- **Flash Messages**: Beautiful notification system for user feedback
- **Railway Deployment Ready**: Configured for easy deployment on Railway

## Pages

1. **Home Page**: Welcome message, social buttons, about section with video, and recent comments
2. **Login Page**: User authentication with beautiful form design
3. **Register Page**: New user registration with validation
4. **Comments Page**: Full comment system with posting and viewing capabilities

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd justaweb
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## Railway Deployment

This application is configured for Railway deployment:

1. **Push to GitHub**: Make sure your code is in a GitHub repository
2. **Connect to Railway**: 
   - Go to [Railway](https://railway.app)
   - Sign up/Login with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
3. **Environment Variables**: Railway will automatically detect the Flask app
4. **Deploy**: Railway will automatically build and deploy your application

### Railway Configuration Files

- `requirements.txt`: Python dependencies
- `Procfile`: Tells Railway how to run the app
- `railway.json`: Railway-specific configuration
- `.gitignore`: Git ignore file

## Customization

### Social Media Links
Update the social media links in `templates/index.html`:
- YouTube: Replace `https://youtube.com` with your YouTube channel
- Kick: Replace `https://kick.com` with your Kick profile
- Discord: Replace `https://discord.com` with your Discord server invite

### YouTube Video
Replace the video ID in `templates/index.html`:
```html
src="https://www.youtube.com/embed/YOUR_VIDEO_ID"
```

### Styling
The main styles are in `static/css/style.css`. You can customize:
- Colors (CSS variables in `:root`)
- Fonts
- Animations
- Layout

## Features in Detail

### Dark Gaming Theme
- Professional dark color scheme
- Neon blue, purple, and green accents
- Custom gradients and shadows
- Smooth hover effects and transitions

### Interactive Elements
- Animated welcome message with typing effect
- Parallax scrolling effects
- Custom cursor with glow effect
- Bounce animations on buttons and indicators

### Security
- Session-based authentication
- Password confirmation validation
- CSRF protection with Flask's built-in features
- Input validation and sanitization

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with CSS Grid and Flexbox
- **Icons**: Font Awesome
- **Fonts**: Google Fonts (Orbitron, Rajdhani)
- **Deployment**: Railway

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge
- Mobile browsers

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues and enhancement requests!