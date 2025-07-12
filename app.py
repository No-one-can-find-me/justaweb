from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Simple in-memory storage for demo purposes
users = {}
comments = []

@app.route('/')
def home():
    return render_template('index.html', comments=comments)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
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
        
        if username in users:
            flash('Username already exists!', 'error')
        elif password != confirm_password:
            flash('Passwords do not match!', 'error')
        elif len(password) < 6:
            flash('Password must be at least 6 characters long!', 'error')
        else:
            users[username] = password
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
            comment = {
                'user': session['user'],
                'text': comment_text,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            comments.append(comment)
            flash('Comment posted successfully!', 'success')
    
    return render_template('comments.html', comments=comments)

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out!', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)