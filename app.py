from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# Replace with your MongoDB connection string
client = MongoClient('mongodb+srv://biswasrayan50:YOUR_PASSWORD_HERE@cluster0.yum2qky.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client.huntsman_space

@app.route('/')
def index():
    comments = db.comments.find()
    return render_template('index.html', comments=comments)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = db.users
        existing_user = users.find_one({'username': request.form['username']})

        if existing_user:
            if existing_user['password'] == request.form['password']:
                return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    users = db.users
    existing_user = users.find_one({'username': request.form['username']})

    if not existing_user:
        users.insert_one({'username': request.form['username'], 'password': request.form['password']})
        return redirect(url_for('login'))
    return 'Username already exists!'

@app.route('/comment', methods=['GET', 'POST'])
def comment():
    if request.method == 'POST':
        comments = db.comments
        comments.insert_one({'comment': request.form['comment']})
        return redirect(url_for('comment'))

    comments = db.comments.find()
    return render_template('comment.html', comments=comments)

if __name__ == '__main__':
    app.run(debug=True)