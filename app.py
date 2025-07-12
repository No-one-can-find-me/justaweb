from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
import os
import json

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# File paths for data storage
USERS_FILE = 'datas/users.txt'
COMMENTS_FILE = 'datas/chats.txt'

# Admin users
ADMIN_USERS = ['huntsmangg']

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
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

def load_comments():
    """Load comments from chats.txt file"""
    try:
        if os.path.exists(COMMENTS_FILE):
            with open(COMMENTS_FILE, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    return json.loads(content)
        return []
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_comments(comments):
    """Save comments to chats.txt file"""
    os.makedirs(os.path.dirname(COMMENTS_FILE), exist_ok=True)
    with open(COMMENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(comments, f, indent=2, ensure_ascii=False)

def get_next_comment_id():
    """Get the next available comment ID"""
    comments = load_comments()
    if not comments:
        return 1
    return max(comment.get('id', 0) for comment in comments) + 1

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
    comments = load_comments()
    return render_template('index.html', comments=comments)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        users = load_users()
        if username in users and users[username] == password:
            session['user'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password!', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        users = load_users()
        if username in users:
            flash('Username already exists!', 'error')
        elif password != confirm_password:
            flash('Passwords do not match!', 'error')
        elif len(password) < 6:
            flash('Password must be at least 6 characters long!', 'error')
        else:
            users[username] = password
            save_users(users)
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/comments', methods=['GET', 'POST'])
def comments_page():
    if request.method == 'POST':
        if 'user' not in session:
            flash('Please login to post comments!', 'error')
            return redirect(url_for('login'))
        
        comment_text = request.form['comment']
        if comment_text.strip():
            comments = load_comments()
            comment = {
                'id': get_next_comment_id(),
                'user': session['user'],
                'text': comment_text,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'replies': []
            }
            comments.append(comment)
            save_comments(comments)
            flash('Comment posted successfully!', 'success')
    
    comments = load_comments()
    return render_template('comments.html', comments=comments)

@app.route('/admin')
def admin_panel():
    if 'user' not in session:
        flash('Please login to access admin panel!', 'error')
        return redirect(url_for('login'))
    
    if session['user'] not in ADMIN_USERS:
        flash('Access denied! Admin privileges required.', 'error')
        return redirect(url_for('home'))
    
    comments = load_comments()
    return render_template('admin.html', comments=comments)

@app.route('/admin/reply/<int:comment_id>', methods=['POST'])
def admin_reply(comment_id):
    if 'user' not in session:
        flash('Please login to reply!', 'error')
        return redirect(url_for('login'))
    
    if session['user'] not in ADMIN_USERS:
        flash('Access denied! Admin privileges required.', 'error')
        return redirect(url_for('home'))
    
    reply_text = request.form['reply']
    if reply_text.strip():
        comments = load_comments()
        # Find the comment to reply to
        for comment in comments:
            if comment['id'] == comment_id:
                reply = {
                    'id': len([r for c in comments for r in c['replies']]) + 1,
                    'user': session['user'],
                    'text': reply_text,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                comment['replies'].append(reply)
                save_comments(comments)
                flash('Reply posted successfully!', 'success')
                break
        else:
            flash('Comment not found!', 'error')
    
    return redirect(url_for('admin_panel'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out!', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)