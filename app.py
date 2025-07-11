from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from pymongo import MongoClient
import hashlib
from datetime import datetime, timedelta
import os
import logging
from bson.objectid import ObjectId
import redis
import json
from functools import wraps
import time

# Configure logging for production
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')

# MongoDB configuration
MONGO_URI = os.environ.get('MONGO_URI', "mongodb+srv://biswasrayan50:LzQzQoP2LpUrvkut@cluster0.yum2qky.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Redis configuration for caching (Railway provides Redis add-on)
REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')

# Configure Flask for production
app.config.update(
    SESSION_COOKIE_SECURE=os.environ.get('FLASK_ENV') == 'production',
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=timedelta(hours=24),
    # Performance optimizations
    SEND_FILE_MAX_AGE_DEFAULT=31536000,  # 1 year cache for static files
    JSON_SORT_KEYS=False,  # Disable JSON key sorting for performance
)

# Initialize Redis client
try:
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    redis_client.ping()
    logger.info("Redis connection established")
except Exception as e:
    logger.warning(f"Redis connection failed: {str(e)}. Caching disabled.")
    redis_client = None

# MongoDB client and database initialization with connection pooling
mongo_client = None
db = None

def get_db():
    """Get MongoDB database connection with connection pooling"""
    global mongo_client, db
    if mongo_client is None:
        try:
            mongo_client = MongoClient(
                MONGO_URI,
                maxPoolSize=50,  # Maximum number of connections
                minPoolSize=5,   # Minimum number of connections
                maxIdleTimeMS=30000,  # Close connections after 30 seconds of inactivity
                serverSelectionTimeoutMS=5000,  # 5 second timeout
                socketTimeoutMS=20000,  # 20 second socket timeout
                connectTimeoutMS=20000,  # 20 second connection timeout
                retryWrites=True
            )
            db = mongo_client.huntsman_space
            logger.info("MongoDB connection pool established")
        except Exception as e:
            logger.error(f"MongoDB connection error: {str(e)}")
            raise
    return db

def init_db():
    """Initialize MongoDB collections and indexes"""
    try:
        database = get_db()
        
        # Create indexes for better performance
        database.users.create_index("username", unique=True)
        database.comments.create_index([("timestamp", -1)])
        
        # Create compound index for better query performance
        database.comments.create_index([("username", 1), ("timestamp", -1)])
        
        logger.info("MongoDB collections initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization error: {str(e)}")

# Cache decorator
def cache_result(timeout=300):  # 5 minutes default
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if redis_client is None:
                return f(*args, **kwargs)
            
            # Create cache key
            cache_key = f"{f.__name__}:{hash(str(args) + str(kwargs))}"
            
            try:
                # Try to get from cache
                cached_result = redis_client.get(cache_key)
                if cached_result:
                    return json.loads(cached_result)
            except Exception as e:
                logger.warning(f"Cache read error: {str(e)}")
            
            # Execute function and cache result
            result = f(*args, **kwargs)
            
            try:
                redis_client.setex(cache_key, timeout, json.dumps(result, default=str))
            except Exception as e:
                logger.warning(f"Cache write error: {str(e)}")
            
            return result
        return decorated_function
    return decorator

# Rate limiting decorator
def rate_limit(max_requests=10, window=60):  # 10 requests per minute
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if redis_client is None:
                return f(*args, **kwargs)
            
            client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
            key = f"rate_limit:{f.__name__}:{client_ip}"
            
            try:
                current = redis_client.get(key)
                if current is None:
                    redis_client.setex(key, window, 1)
                elif int(current) >= max_requests:
                    return jsonify({'error': 'Rate limit exceeded'}), 429
                else:
                    redis_client.incr(key)
            except Exception as e:
                logger.warning(f"Rate limiting error: {str(e)}")
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Helper function to get comments with caching
@cache_result(timeout=60)  # Cache for 1 minute
def get_comments():
    try:
        database = get_db()
        comments = list(database.comments.find().sort("timestamp", -1).limit(50))  # Limit to 50 comments
        
        # Convert ObjectId to string and format timestamp for display
        for comment in comments:
            comment['_id'] = str(comment['_id'])
            if 'timestamp' in comment and comment['timestamp']:
                comment['timestamp'] = comment['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
            
        return comments
    except Exception as e:
        logger.error(f"Error fetching comments: {str(e)}")
        return []

# Health check endpoint
@app.route('/health')
def health_check():
    """Health check endpoint for Railway"""
    try:
        # Test database connection
        database = get_db()
        database.command('ping')
        
        # Test Redis connection
        redis_status = "connected" if redis_client and redis_client.ping() else "disconnected"
        
        return {
            'status': 'healthy',
            'message': 'Application is running',
            'database': 'connected',
            'cache': redis_status,
            'timestamp': datetime.utcnow().isoformat()
        }, 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            'status': 'unhealthy',
            'message': 'Database connection failed',
            'timestamp': datetime.utcnow().isoformat()
        }, 503

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('base.html'), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {str(error)}")
    return render_template('base.html'), 500

@app.errorhandler(429)
def rate_limit_error(error):
    return jsonify({'error': 'Rate limit exceeded. Please try again later.'}), 429

# Routes
@app.route('/')
def home():
    try:
        comments = get_comments()
        return render_template('index.html', comments=comments)
    except Exception as e:
        logger.error(f"Error loading home page: {str(e)}")
        return render_template('index.html', comments=[])

@app.route('/login', methods=['GET', 'POST'])
@rate_limit(max_requests=5, window=300)  # 5 login attempts per 5 minutes
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            flash('Username and password are required!', 'error')
            return render_template('login.html')
        
        try:
            database = get_db()
            user = database.users.find_one({
                'username': username,
                'password': hash_password(password)
            })
            
            if user:
                session['username'] = username
                session.permanent = True
                flash('Login successful!', 'success')
                
                # Clear comments cache to refresh user-specific content
                if redis_client:
                    try:
                        redis_client.delete('get_comments:*')
                    except:
                        pass
                
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password!', 'error')
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            flash('Login failed. Please try again.', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
@rate_limit(max_requests=3, window=300)  # 3 registration attempts per 5 minutes
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
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
            database = get_db()
            
            # Check if username already exists
            existing_user = database.users.find_one({'username': username})
            if existing_user:
                flash('Username already exists!', 'error')
                return render_template('register.html')
            
            # Create new user
            user_data = {
                'username': username,
                'password': hash_password(password),
                'created_at': datetime.utcnow()
            }
            
            database.users.insert_one(user_data)
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
        
        comment_text = request.form.get('comment', '').strip()
        if len(comment_text) == 0:
            flash('Comment cannot be empty!', 'error')
        elif len(comment_text) > 1000:  # Limit comment length
            flash('Comment is too long! Maximum 1000 characters.', 'error')
        else:
            try:
                database = get_db()
                comment_data = {
                    'username': session['username'],
                    'text': comment_text,
                    'timestamp': datetime.utcnow()
                }
                
                database.comments.insert_one(comment_data)
                flash('Comment posted successfully!', 'success')
                
                # Clear comments cache
                if redis_client:
                    try:
                        for key in redis_client.scan_iter(match="get_comments:*"):
                            redis_client.delete(key)
                    except:
                        pass
                
            except Exception as e:
                logger.error(f"Comment posting error: {str(e)}")
                flash('Failed to post comment. Please try again.', 'error')
        
        return redirect(url_for('comments_page'))
    
    comments = get_comments()
    return render_template('comments.html', comments=comments)

# API endpoint for comments (for potential AJAX loading)
@app.route('/api/comments')
@cache_result(timeout=30)  # Cache for 30 seconds
def api_comments():
    try:
        comments = get_comments()
        return jsonify({'comments': comments, 'status': 'success'})
    except Exception as e:
        logger.error(f"API comments error: {str(e)}")
        return jsonify({'error': 'Failed to fetch comments', 'status': 'error'}), 500

# Static file caching
@app.after_request
def after_request(response):
    # Add security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # Add caching headers for static files
    if request.endpoint == 'static':
        response.headers['Cache-Control'] = 'public, max-age=31536000'  # 1 year
    
    return response

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)