from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
import hashlib
from datetime import datetime
import os
import logging
from bson.objectid import ObjectId

# Configure logging for production
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')

# MongoDB configuration
MONGO_URI = "mongodb+srv://biswasrayan50:LzQzQoP2LpUrvkut@cluster0.yum2qky.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Configure Flask for production
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# MongoDB client and database initialization
def get_db():
    """Get MongoDB database connection"""
    try:
        client = MongoClient(MONGO_URI)
        db = client.huntsman_space  # Database name
        return db
    except Exception as e:
        logger.error(f"MongoDB connection error: {str(e)}")
        raise

def init_db():
    """Initialize MongoDB collections and indexes"""
    try:
        db = get_db()
        
        # Create indexes for better performance
        # Users collection - unique index on username
        db.users.create_index("username", unique=True)
        
        # Comments collection - index on timestamp for sorting
        db.comments.create_index([("timestamp", -1)])
        
        logger.info("MongoDB collections initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization error: {str(e)}")

# Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Helper function to get comments
def get_comments():
    try:
        db = get_db()
        comments = list(db.comments.find().sort("timestamp", -1))
        
        # Convert ObjectId to string and format timestamp for display
        for comment in comments:
            comment['_id'] = str(comment['_id'])
            # Format timestamp for better display
            if 'timestamp' in comment and comment['timestamp']:
                comment['timestamp'] = comment['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
            
        return comments
    except Exception as e:
        logger.error(f"Error fetching comments: {str(e)}")
        return []

@app.route('/health')
def health_check():
    """Health check endpoint for Koyeb"""
    try:
        # Test database connection
        db = get_db()
        db.command('ping')
        return {'status': 'healthy', 'message': 'Application is running', 'database': 'connected'}, 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {'status': 'unhealthy', 'message': 'Database connection failed'}, 503

@app.errorhandler(404)
def not_found_error(error):
    return render_template('base.html'), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {str(error)}")
    return render_template('base.html'), 500

@app.route('/')
def home():
    try:
        comments = get_comments()
        return render_template('index.html', comments=comments)
    except Exception as e:
        logger.error(f"Error loading home page: {str(e)}")
        return render_template('index.html', comments=[])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            db = get_db()
            user = db.users.find_one({
                'username': username,
                'password': hash_password(password)
            })
            
            if user:
                session['username'] = username
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password!', 'error')
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            flash('Login failed. Please try again.', 'error')
    
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
        
        try:
            db = get_db()
            
            # Check if username already exists
            existing_user = db.users.find_one({'username': username})
            if existing_user:
                flash('Username already exists!', 'error')
                return render_template('register.html')
            
            # Create new user
            user_data = {
                'username': username,
                'password': hash_password(password),
                'created_at': datetime.utcnow()
            }
            
            db.users.insert_one(user_data)
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            flash('Registration failed. Please try again.', 'error')
    
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
            try:
                db = get_db()
                comment_data = {
                    'username': session['username'],
                    'text': comment_text,
                    'timestamp': datetime.utcnow()
                }
                
                db.comments.insert_one(comment_data)
                flash('Comment posted successfully!', 'success')
                
            except Exception as e:
                logger.error(f"Comment posting error: {str(e)}")
                flash('Failed to post comment. Please try again.', 'error')
        
        return redirect(url_for('comments_page'))
    
    comments = get_comments()
    return render_template('comments.html', comments=comments)

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)