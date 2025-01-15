from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize the Flask app
app = Flask(__name__)

# Set the URI for the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disables modification tracking
app.config['SECRET_KEY'] = 'your_secret_key_here'  # For sessions and security

# Initialize the SQLAlchemy object here
db = SQLAlchemy(app)

# Database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Transaction {self.amount} {self.category}>'

# Create the database tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    transactions = Transaction.query.all()
    return render_template('index.html', transactions=transactions)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')

        new_user = User(username=username, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash("User Registered Successfully!")
            return redirect(url_for('login'))
        except:
            db.session.rollback()
            flash("Error! Please try again.")
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            flash("Login Successful!")
            return redirect(url_for('index'))
        else:
            flash("Invalid credentials!")
    return render_template('login.html')

@app.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        amount = request.form['amount']
        category = request.form['category']
        date = request.form['date']
        description = request.form['description']
        user_id = 1  # Assuming the user is logged in, set user_id to 1 for now

        new_transaction = Transaction(amount=amount, category=category, date=date, description=description, user_id=user_id)
        try:
            db.session.add(new_transaction)
            db.session.commit()
            flash("Transaction Added Successfully!")
            return redirect(url_for('index'))
        except:
            db.session.rollback()
            flash("Error! Please try again.")
    return render_template('add_transaction.html')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
