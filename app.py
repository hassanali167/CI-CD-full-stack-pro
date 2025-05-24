
from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "secret_key"

# Connect to MongoDB
client =MongoClient("mongodb://mongodb:27017/")
db = client.user_database
users_collection = db.users

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = users_collection.find_one({'username': username, 'password': password})
    if user:
        session['username'] = username
        return redirect(url_for('welcome'))
    else:
        return "Invalid username or password! Please <a href='/'>try again</a>."

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users_collection.find_one({'username': username}):
            return "Username already exists! Please <a href='/register'>try another</a>."
        users_collection.insert_one({'username': username, 'password': password})
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/welcome')
def welcome():
    if 'username' in session:
        return render_template('welcome.html', username=session['username'])
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

