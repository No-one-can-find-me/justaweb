from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import hashlib
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')

# Database path - use /tmp for ephemeral storage on Koyeb
DB_PATH = os.environ.get('DATABASE_PATH', '/tmp/database.db')

# Database initialization
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create comments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            text TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Helper function to get comments
def get_comments():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT username, text, timestamp FROM comments ORDER BY timestamp DESC')
    comments = []
    for row in cursor.fetchall():
        comments.append({
            'username': row[0],
            'text': row[1],
            'timestamp': row[2]
        })
    conn.close()
    return comments

@app.route('/health')
def health_check():
    """Health check endpoint for Koyeb"""
    return {'status': 'healthy', 'message': 'Application is running'}, 200

@app.route('/')
def home():
    try:
        comments = get_comments()
        return render_template('index.html', comments=comments)
    except Exception as e:
        # Initialize database if it doesn't exist
        init_db()
        comments = get_comments()
        return render_template('index.html', comments=comments)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT username FROM users WHERE username = ? AND password = ?', 
                      (username, hash_password(password)))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['username'] = username
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
        
        if len(username) < 3:
            flash('Username must be at least 3 characters long!', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long!', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template('register.html')
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                          (username, hash_password(password)))
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists!', 'error')
        finally:
            conn.close()
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out!', 'info')
    return redirect(url_for('home'))

@app.route('/comments', methods=['GET', 'POST'])
def comments_page():
    if request.method == 'POST':
        if 'username' not in session:
            flash('Please login to post a comment!', 'error')
            return redirect(url_for('login'))
        
        comment_text = request.form['comment']
        if len(comment_text.strip()) == 0:
            flash('Comment cannot be empty!', 'error')
        else:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO comments (username, text) VALUES (?, ?)', 
                          (session['username'], comment_text))
            conn.commit()
            conn.close()
            flash('Comment posted successfully!', 'success')
        
        return redirect(url_for('comments_page'))
    
    comments = get_comments()
    return render_template('comments.html', comments=comments)

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)