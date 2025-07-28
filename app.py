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
REDEEM_CODES_FILE = 'datas/redeem_codes.txt'
SHOP_ITEMS_FILE = 'datas/shop_items.txt'

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
    try:
        os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving users: {e}")
        # In production, you'd want to log this properly
        
def get_user_data(username):
    """Get user data including profile information"""
    users = load_users()
    
    # If username exists in users dict
    if username in users:
        # If it's a string, it's the old format with just password
        if isinstance(users[username], str):
            # Convert to new format
            password = users[username]
            users[username] = {
                'password': password,
                'display_name': None,
                'bio': None,
                'joined_date': datetime.now().strftime('%Y-%m-%d'),
                'coins': 0  # Initialize coins to 0
            }
            save_users(users)
        
        # Return user data
        return users[username]
    
    return None



# Initialize with admin user if users.txt is empty
def load_redeem_codes():
    """Load redeem codes from redeem_codes.txt file"""
    try:
        if os.path.exists(REDEEM_CODES_FILE):
            with open(REDEEM_CODES_FILE, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    return json.loads(content)
        return {}
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_redeem_codes(codes):
    """Save redeem codes to redeem_codes.txt file"""
    try:
        os.makedirs(os.path.dirname(REDEEM_CODES_FILE), exist_ok=True)
        with open(REDEEM_CODES_FILE, 'w', encoding='utf-8') as f:
            json.dump(codes, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving redeem codes: {e}")

def load_shop_items():
    """Load shop items from shop_items.txt file"""
    try:
        if os.path.exists(SHOP_ITEMS_FILE):
            with open(SHOP_ITEMS_FILE, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    return json.loads(content)
        return []
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_shop_items(items):
    """Save shop items to shop_items.txt file"""
    try:
        os.makedirs(os.path.dirname(SHOP_ITEMS_FILE), exist_ok=True)
        with open(SHOP_ITEMS_FILE, 'w', encoding='utf-8') as f:
            json.dump(items, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving shop items: {e}")

def load_messages():
    """Load messages from messages file (placeholder for chat functionality)"""
    # For now, return empty list since chat isn't fully implemented
    return []

def save_messages(messages):
    """Save messages to messages file (placeholder for chat functionality)"""
    # For now, do nothing since chat isn't fully implemented
    pass

def get_next_message_id():
    """Get next message ID (placeholder for chat functionality)"""
    # For now, return a simple timestamp-based ID
    return int(datetime.now().timestamp() * 1000)

def initialize_admin_user():
    """Initialize admin user if not exists"""
    users = load_users()
    if 'huntsmangg' not in users:
        users['huntsmangg'] = {
            'password': '1976Abcd?',
            'display_name': 'Huntsman',
            'bio': 'Admin and creator of Huntsman Space',
            'joined_date': datetime.now().strftime('%Y-%m-%d'),
            'coins': 1000  # Give admin some initial coins
        }
        save_users(users)
    elif isinstance(users['huntsmangg'], str):
        # Convert old format to new format
        password = users['huntsmangg']
        users['huntsmangg'] = {
            'password': password,
            'display_name': 'Huntsman',
            'bio': 'Admin and creator of Huntsman Space',
            'joined_date': datetime.now().strftime('%Y-%m-%d'),
            'coins': 1000  # Give admin some initial coins
        }
        save_users(users)
    elif 'coins' not in users['huntsmangg']:
        # Add coins field if it doesn't exist
        users['huntsmangg']['coins'] = 1000
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
        
        if user_found:
            # Check if user data is in the new format or old format
            if isinstance(users[user_found], dict):
                stored_password = users[user_found]['password']
            else:
                stored_password = users[user_found]
                
            if stored_password == password:
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
                # Store user with new format including profile data
                users[username] = {
                    'password': password,
                    'display_name': None,
                    'bio': None,
                    'joined_date': datetime.now().strftime('%Y-%m-%d'),
                    'coins': 0  # Initialize coins to 0
                }
                save_users(users)
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('login'))
    
    return render_template('register.html')



@app.route('/profile')
def profile():
    if 'user' not in session:
        flash('Please login to access your profile!', 'error')
        return redirect(url_for('login'))
    
    # Get user data including profile information
    user_data = get_user_data(session['user'])
    if not user_data:
        # This should not happen, but just in case
        flash('User data not found!', 'error')
        return redirect(url_for('logout'))
    
    return render_template('profile.html', user_data=user_data)

@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'user' not in session:
        flash('Please login to update your profile!', 'error')
        return redirect(url_for('login'))
    
    # Get form data
    display_name = request.form.get('display_name', '').strip()
    new_username = request.form.get('username', '').strip()
    bio = request.form.get('bio', '').strip()
    
    # Validate input
    if len(display_name) > 30:
        flash('Display name must be 30 characters or less!', 'error')
        return redirect(url_for('profile'))
    
    if len(bio) > 200:
        flash('Bio must be 200 characters or less!', 'error')
        return redirect(url_for('profile'))
    
    # Load users data
    users = load_users()
    current_username = session['user']
    
    # Check if username exists and is different from current
    if new_username != current_username:
        # Validate new username
        if not new_username or len(new_username) < 3:
            flash('Username must be at least 3 characters long!', 'error')
            return redirect(url_for('profile'))
        elif len(new_username) > 20:
            flash('Username must be 20 characters or less!', 'error')
            return redirect(url_for('profile'))
        elif not new_username.isalnum():
            flash('Username can only contain letters and numbers!', 'error')
            return redirect(url_for('profile'))
        elif new_username.lower() in [u.lower() for u in users.keys() if u.lower() != current_username.lower()]:
            flash('Username already exists!', 'error')
            return redirect(url_for('profile'))
        else:
            # Create new user entry with same data
            users[new_username] = users[current_username]
            # Delete old username
            del users[current_username]
            # Update session
            session['user'] = new_username
            flash('Username updated successfully!', 'success')
    else:
        # If user data is in old format, convert it
        if isinstance(users[current_username], str):
            password = users[current_username]
            users[current_username] = {
                'password': password,
                'display_name': None,
                'bio': None,
                'joined_date': datetime.now().strftime('%Y-%m-%d'),
                'coins': 0  # Initialize coins to 0
            }
        
        # Update display name, bio, and coins
        if 'display_name' not in users[current_username]:
            users[current_username]['display_name'] = None
        if 'bio' not in users[current_username]:
            users[current_username]['bio'] = None
        if 'coins' not in users[current_username]:
            users[current_username]['coins'] = 0
        
        users[current_username]['display_name'] = display_name if display_name else None
        users[current_username]['bio'] = bio if bio else None
        
        flash('Profile updated successfully!', 'success')
    
    # Save updated users data
    save_users(users)
    
    return redirect(url_for('profile'))

@app.route('/logout')
def logout():
    if 'user' in session:
        session.clear()  # Clear all session data
        flash('You have been logged out!', 'info')
    return redirect(url_for('home'))



@app.route('/get_user_profile')
def get_user_profile():
    """Get user profile information"""
    if 'user' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
    
    username = request.args.get('username')
    if not username:
        return jsonify({'success': False, 'error': 'Username is required'}), 400
    
    # Get user data
    user_data = get_user_data(username)
    if not user_data:
        return jsonify({'success': False, 'error': 'User not found'}), 404
    
    # Check friendship status
    current_user = session['user']
    is_friend = False
    friend_request_sent = False
    friend_request_received = False
    
    # In a real implementation, we would check the friendship status in a database
    # For now, we'll just return placeholder values
    
    return jsonify({
        'success': True,
        'username': username,
        'display_name': user_data.get('display_name'),
        'bio': user_data.get('bio'),
        'joined_date': user_data.get('joined_date'),
        'is_admin': username in ADMIN_USERS,
        'is_friend': is_friend,
        'friend_request_sent': friend_request_sent,
        'friend_request_received': friend_request_received
    })

@app.route('/send_friend_request', methods=['POST'])
def send_friend_request():
    """Send a friend request to another user"""
    if 'user' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
    
    data = request.get_json()
    if not data or 'username' not in data:
        return jsonify({'success': False, 'error': 'Username is required'}), 400
    
    target_username = data['username']
    current_username = session['user']
    
    # Don't allow sending friend requests to yourself
    if target_username == current_username:
        return jsonify({'success': False, 'error': 'You cannot send a friend request to yourself'}), 400
    
    # Check if target user exists
    user_data = get_user_data(target_username)
    if not user_data:
        return jsonify({'success': False, 'error': 'User not found'}), 404
    
    # In a real implementation, we would store the friend request in a database
    # For now, we'll just return success
    
    return jsonify({
        'success': True,
        'message': f'Friend request sent to {target_username}'
    })

@app.route('/search_users')
def search_users():
    """Search for users by username"""
    if 'user' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
    
    query = request.args.get('query', '').lower()
    if not query or len(query) < 2:
        return jsonify({'success': False, 'error': 'Query must be at least 2 characters'}), 400
    
    # Get all users
    users = load_users()
    
    # Filter users by query
    matching_users = []
    for username in users:
        if query in username.lower():
            matching_users.append({
                'username': username,
                'is_admin': username in ADMIN_USERS
            })
    
    return jsonify({
        'success': True,
        'users': matching_users
    })

@app.route('/static/images/profile_icon.jpg')
def serve_profile_image():
    """Serve profile image with proper caching headers"""
    response = send_from_directory('static/images', 'profile_icon.jpg')
    # Set cache headers for better performance
    response.headers['Cache-Control'] = 'public, max-age=604800'  # Cache for 7 days
    response.headers['ETag'] = 'profile-icon-v2'
    return response

@app.route('/static/images/website_logo.png')
def serve_website_logo():
    """Serve website logo with proper caching headers"""
    # If the file doesn't exist yet, serve the profile icon as a fallback
    try:
        response = send_from_directory('static/images', 'website_logo.png')
    except:
        return serve_profile_image()
    
    # Set cache headers for better performance
    response.headers['Cache-Control'] = 'public, max-age=604800'  # Cache for 7 days
    response.headers['ETag'] = 'website-logo-v1'
    return response

@app.route('/redeem', methods=['GET', 'POST'])
def redeem_code():
    if 'user' not in session:
        flash('Please login to redeem codes!', 'error')
        return redirect(url_for('login'))
    
    user_data = get_user_data(session['user'])
    
    if request.method == 'POST':
        code = request.form.get('code', '').strip()
        
        if not code:
            flash('Please enter a valid redeem code!', 'error')
            return render_template('redeem.html', user_data=user_data, shop_items=load_shop_items())
            
        # Validate redeem code length
        if len(code) < 4 or len(code) > 16:
            flash('Redeem code must be between 4 and 16 characters long!', 'error')
            return render_template('redeem.html', user_data=user_data, shop_items=load_shop_items())
        
        # Load redeem codes
        redeem_codes = load_redeem_codes()
        
        if code not in redeem_codes:
            flash('Invalid redeem code!', 'error')
            return render_template('redeem.html', user_data=user_data, shop_items=load_shop_items())
        
        code_data = redeem_codes[code]
        
        # Check if code is expired
        expiry_time = datetime.fromisoformat(code_data['expiry_time'])
        if datetime.now() > expiry_time:
            flash('This redeem code has expired!', 'error')
            return render_template('redeem.html', user_data=user_data, shop_items=load_shop_items())
        
        # Check if maximum claims reached
        if len(code_data['claimed_by']) >= code_data['max_claims']:
            flash('This redeem code has reached its maximum claims!', 'error')
            return render_template('redeem.html', user_data=user_data, shop_items=load_shop_items())
        
        # Check if user already claimed this code
        if session['user'] in code_data['claimed_by']:
            flash('You have already claimed this code!', 'error')
            return render_template('redeem.html', user_data=user_data, shop_items=load_shop_items())
        
        # All checks passed, redeem the code
        users = load_users()
        
        # Initialize coins if not present
        if 'coins' not in users[session['user']]:
            users[session['user']]['coins'] = 0
        
        # Add coins to user
        users[session['user']]['coins'] += code_data['coin_value']
        
        # Add user to claimed list
        code_data['claimed_by'].append(session['user'])
        
        # Save changes
        save_users(users)
        save_redeem_codes(redeem_codes)
        
        flash(f'Successfully redeemed code for {code_data["coin_value"]} coins!', 'success')
        
        # Update user data for template
        user_data = get_user_data(session['user'])
        return redirect(url_for('redeem_code'))
    
    # Load shop items
    shop_items = load_shop_items()
    
    return render_template('redeem.html', user_data=user_data, shop_items=shop_items)

@app.route('/shop')
def shop():
    if 'user' not in session:
        flash('Please login to access the shop!', 'error')
        return redirect(url_for('login'))
    
    user_data = get_user_data(session['user'])
    shop_items = load_shop_items()
    
    return render_template('shop.html', user_data=user_data, shop_items=shop_items)

@app.route('/minigames')
def minigames():
    return render_template('minigames.html')

@app.route('/chat')
def chat():
    if 'user' not in session:
        flash('Please login to access the chat!', 'error')
        return redirect(url_for('login'))
    
    # For now, redirect to home since chat functionality isn't implemented yet
    flash('Chat feature coming soon!', 'info')
    return redirect(url_for('home'))

@app.route('/purchase', methods=['POST'])
def purchase_item():
    if 'user' not in session:
        flash('Please login to purchase items!', 'error')
        return redirect(url_for('login'))
    
    # Get form data
    item_id = request.form.get('item_id')
    email = request.form.get('email')
    
    if not item_id or not email:
        flash('Missing required information!', 'error')
        return redirect(url_for('redeem_code'))
    
    # Load shop items and user data
    shop_items = load_shop_items()
    users = load_users()
    user_data = users[session['user']]
    
    # Find the item
    item = None
    for shop_item in shop_items:
        if str(shop_item['id']) == str(item_id):
            item = shop_item
            break
    
    if not item:
        flash('Item not found!', 'error')
        return redirect(url_for('redeem_code'))
    
    # Check if user has enough coins
    if 'coins' not in user_data:
        user_data['coins'] = 0
    
    if user_data['coins'] < item['price']:
        flash('You do not have enough coins to purchase this item!', 'error')
        return redirect(url_for('redeem_code'))
    
    # Deduct coins from user
    user_data['coins'] -= item['price']
    
    # Save updated user data
    save_users(users)
    
    # Send notification to admin via chat
    purchase_message = {
        'id': get_next_message_id(),
        'user': 'system',
        'message': f"PURCHASE NOTIFICATION: User '{session['user']}' purchased '{item['name']}' for {item['price']} coins. Email: {email}",
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'channel': 'general',
        'profile_picture': None
    }
    
    messages = load_messages()
    messages.append(purchase_message)
    save_messages(messages)
    
    flash(f'Successfully purchased {item["name"]}! Check your email for details.', 'success')
    return redirect(url_for('shop'))

@app.route('/add-shop-item', methods=['POST'])
def add_shop_item():
    if 'user' not in session or session['user'] not in ADMIN_USERS:
        flash('You do not have permission to add shop items!', 'error')
        return redirect(url_for('profile'))
    
    # Get form data
    item_name = request.form.get('item_name', '').strip()
    item_price = request.form.get('item_price', '')
    item_validity = request.form.get('item_validity', '')
    item_image = request.form.get('item_image', '').strip()
    
    # Validate inputs
    if not item_name or not item_price or not item_validity or not item_image:
        flash('All fields are required!', 'error')
        return redirect(url_for('profile'))
    
    try:
        item_price = int(item_price)
        item_validity = int(item_validity)
    except ValueError:
        flash('Price and validity must be numbers!', 'error')
        return redirect(url_for('profile'))
    
    # Load existing shop items
    shop_items = load_shop_items()
    
    # Generate a new item ID
    item_id = 1
    if shop_items:
        item_id = max(item['id'] for item in shop_items) + 1
    
    # Create new item
    new_item = {
        'id': item_id,
        'name': item_name,
        'price': item_price,
        'validity': item_validity,
        'image': item_image
    }
    
    # Add to shop items
    shop_items.append(new_item)
    
    # Save shop items
    save_shop_items(shop_items)
    
    flash(f'Successfully added {item_name} to the shop!', 'success')
    return redirect(url_for('profile'))

@app.route('/create-redeem-code', methods=['POST'])
def create_redeem_code():
    if 'user' not in session or session['user'] not in ADMIN_USERS:
        flash('You do not have permission to create redeem codes!', 'error')
        return redirect(url_for('profile'))
    
    redeem_code = request.form.get('redeem_code', '').strip()
    coin_value = request.form.get('coin_value', '')
    max_claims = request.form.get('max_claims', '')
    expiry_hours = request.form.get('expiry_hours', '')
    
    # Validate inputs
    if not redeem_code or not coin_value or not max_claims or not expiry_hours:
        flash('All fields are required!', 'error')
        return redirect(url_for('profile'))
    
    # Validate redeem code length
    if len(redeem_code) < 4 or len(redeem_code) > 16:
        flash('Redeem code must be between 4 and 16 characters long!', 'error')
        return redirect(url_for('profile'))
    
    try:
        coin_value = int(coin_value)
        max_claims = int(max_claims)
        expiry_hours = int(expiry_hours)
        
        if coin_value < 1 or max_claims < 1 or expiry_hours < 1:
            flash('Values must be positive numbers!', 'error')
            return redirect(url_for('profile'))
    except ValueError:
        flash('Invalid number format!', 'error')
        return redirect(url_for('profile'))
    
    # Load existing redeem codes
    redeem_codes = load_redeem_codes()
    
    # Check if code already exists
    if redeem_code in redeem_codes:
        flash('This redeem code already exists!', 'error')
        return redirect(url_for('profile'))
    
    # Create new redeem code
    expiry_time = datetime.now() + timedelta(hours=expiry_hours)
    
    redeem_codes[redeem_code] = {
        'coin_value': coin_value,
        'max_claims': max_claims,
        'expiry_time': expiry_time.isoformat(),
        'created_by': session['user'],
        'created_at': datetime.now().isoformat(),
        'claimed_by': []
    }
    
    # Save redeem codes
    save_redeem_codes(redeem_codes)
    
    flash(f'Redeem code "{redeem_code}" created successfully!', 'success')
    return redirect(url_for('profile'))

if __name__ == '__main__':
    app.run(debug=True)