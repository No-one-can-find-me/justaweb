from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory
from datetime import datetime, timedelta
import os
import json

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Session configuration
app.permanent_session_lifetime = timedelta(hours=24)  # Session expires after 24 hours

# File paths for data storage
USERS_FILE = 'datas/users.txt'
COMMENTS_FILE = 'datas/chats.txt'

# Admin users
ADMIN_USERS = ['huntsmangg']

# Rate limiting: Store last message time per user
user_last_message = {}

# Track active users (in real app, you'd use Redis or a database)
active_users = {}

def load_users():
    """Load users from users.txt file"""
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    return json.loads(content)
        return {}
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_users(users):
    """Save users to users.txt file"""
    try:
        os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving users: {e}")
        # In production, you'd want to log this properly

def load_messages():
    """Load messages from chats.txt file and enhance with profile picture info"""
    try:
        if os.path.exists(COMMENTS_FILE):
            with open(COMMENTS_FILE, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    messages = json.loads(content)
                    # Enhance messages with profile picture information
                    for message in messages:
                        message['profile_picture'] = get_user_profile_picture(message.get('user', ''))
                    return messages
        return []
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def get_user_profile_picture(username):
    """Get profile picture path for a user"""
    if username == 'huntsmangg':
        return None  # Admin uses crown icon
    else:
        # Check if profile image exists
        profile_path = 'static/images/profile_icon.jpg'
        if os.path.exists(profile_path):
            return '/static/images/profile_icon.jpg'
        else:
            # Fallback to a default placeholder if image doesn't exist
            return None

def update_user_activity(username):
    """Update user's last activity time"""
    active_users[username] = {
        'last_seen': datetime.now(),
        'is_admin': username in ADMIN_USERS,
        'profile_picture': get_user_profile_picture(username)
    }

def get_active_members():
    """Get list of currently active members (active in last 5 minutes)"""
    cutoff_time = datetime.now() - timedelta(minutes=5)
    active_members = []
    
    # Clean up old entries and collect active users
    users_to_remove = []
    for username, data in active_users.items():
        if data['last_seen'] > cutoff_time:
            active_members.append({
                'username': username,
                'is_admin': data['is_admin'],
                'profile_picture': data['profile_picture'],
                'last_seen': data['last_seen'].strftime('%Y-%m-%d %H:%M:%S')
            })
        else:
            users_to_remove.append(username)
    
    # Remove inactive users
    for username in users_to_remove:
        del active_users[username]
    
    return active_members

def save_messages(messages):
    """Save messages to chats.txt file"""
    try:
        os.makedirs(os.path.dirname(COMMENTS_FILE), exist_ok=True)
        with open(COMMENTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(messages, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving messages: {e}")
        # In production, you'd want to log this properly

def get_next_message_id():
    """Get the next available message ID"""
    messages = load_messages()
    if not messages:
        return 1
    return max(msg.get('id', 0) for msg in messages) + 1

# Initialize with admin user if users.txt is empty
def initialize_admin_user():
    """Initialize admin user if not exists"""
    users = load_users()
    if 'huntsmangg' not in users:
        users['huntsmangg'] = '1976Abcd?'
        save_users(users)

# Initialize admin user on startup
initialize_admin_user()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        
        # Basic input validation
        if not username or not password:
            flash('Please enter both username and password!', 'error')
            return render_template('login.html')
        
        users = load_users()
        # Case-insensitive username check for login
        user_found = None
        for stored_user in users:
            if stored_user.lower() == username.lower():
                user_found = stored_user
                break
        
        if user_found and users[user_found] == password:
            session.permanent = True  # Make session permanent (uses permanent_session_lifetime)
            session['user'] = user_found  # Use the exact stored username
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password!', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Enhanced validation
        if not username or len(username) < 3:
            flash('Username must be at least 3 characters long!', 'error')
        elif len(username) > 20:
            flash('Username must be 20 characters or less!', 'error')
        elif not username.isalnum():
            flash('Username can only contain letters and numbers!', 'error')
        elif not password or len(password) < 6:
            flash('Password must be at least 6 characters long!', 'error')
        elif password != confirm_password:
            flash('Passwords do not match!', 'error')
        else:
            users = load_users()
            if username.lower() in [u.lower() for u in users.keys()]:
                flash('Username already exists!', 'error')
            else:
                users[username] = password
                save_users(users)
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/chat')
def chat():
    if 'user' not in session:
        flash('Please login to access chat!', 'error')
        return redirect(url_for('login'))
    
    # Update user activity when accessing chat
    update_user_activity(session['user'])
    
    messages = load_messages()
    return render_template('chat.html', messages=messages)

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'user' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Invalid JSON data'}), 400
        
        message_text = data.get('message', '').strip()
    except Exception as e:
        return jsonify({'success': False, 'error': 'Invalid request format'}), 400
    
    if not message_text:
        return jsonify({'success': False, 'error': 'Message cannot be empty'}), 400
    
    if len(message_text) > 2000:
        return jsonify({'success': False, 'error': 'Message too long (max 2000 characters)'}), 400
    
    # Rate limiting: Prevent spam (1 message per 2 seconds, except admins)
    current_user = session['user']
    current_time = datetime.now()
    if current_user not in ADMIN_USERS:
        if current_user in user_last_message:
            time_diff = current_time - user_last_message[current_user]
            if time_diff < timedelta(seconds=0.001):
                return jsonify({'success': False, 'error': 'Please wait before sending another message'}), 429
        
    user_last_message[current_user] = current_time
    
    messages = load_messages()
    message = {
        'id': get_next_message_id(),
        'user': session['user'],
        'text': message_text,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'profile_picture': get_user_profile_picture(session['user'])
    }
    
    messages.append(message)
    save_messages(messages)
    
    return jsonify({'success': True, 'message': message})





@app.route('/get_messages')
def get_messages():
    if 'user' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
    
    messages = load_messages()
    return jsonify({'success': True, 'messages': messages})

@app.route('/get_new_messages')
def get_new_messages():
    if 'user' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
    
    # Update user activity on each poll
    update_user_activity(session['user'])
    
    since_id = request.args.get('since', 0, type=int)
    messages = load_messages()
    
    # Get all current message IDs
    current_message_ids = [msg.get('id', 0) for msg in messages]
    
    # Filter messages newer than the specified ID
    new_messages = [msg for msg in messages if msg.get('id', 0) > since_id]
    
    return jsonify({
        'success': True, 
        'messages': new_messages,
        'current_message_ids': current_message_ids
    })

@app.route('/profile')
def profile():
    if 'user' not in session:
        flash('Please login to access your profile!', 'error')
        return redirect(url_for('login'))
    
    return render_template('profile.html')

@app.route('/logout')
def logout():
    if 'user' in session:
        user = session['user']
        session.clear()  # Clear all session data
        # Clean up rate limiting data for logged out user
        if user in user_last_message:
            del user_last_message[user]
        flash('You have been logged out!', 'info')
    return redirect(url_for('home'))

@app.route('/get_members')
def get_members():
    """Get list of active members"""
    if 'user' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
    
    # Update current user's activity
    update_user_activity(session['user'])
    
    # Get active members
    members = get_active_members()
    
    return jsonify({
        'success': True,
        'members': members
    })

@app.route('/static/images/profile_icon.jpg')
def serve_profile_image():
    """Serve profile image with proper caching headers"""
    response = send_from_directory('static/images', 'profile_icon.jpg')
    # Set cache headers for better performance
    response.headers['Cache-Control'] = 'public, max-age=86400'  # Cache for 24 hours
    response.headers['ETag'] = 'profile-icon-v1'
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    # Disable debug mode in production
    debug_mode = os.environ.get('FLASK_ENV', 'development') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
