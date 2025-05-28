from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Database Models
class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(200))
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    cards = db.relationship('Card', backref='author', lazy=True)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Routes
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        
        if Users.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password)
        new_user = Users(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user = Users.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index')
@login_required
def index():
    cards = Card.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', cards=cards)

@app.route('/card/<int:id>')
@login_required
def card(id):
    card = Card.query.get_or_404(id)
    if card.user_id != current_user.id:
        flash('You can only view your own cards', 'error')
        return redirect(url_for('index'))
    return render_template('card.html', card=card)

@app.route('/create')
@login_required
def create():
    return render_template('create.html')

@app.route('/form_create', methods=['GET','POST'])
@login_required
def form_create():
    if request.method == "POST":
        title = request.form.get('title')
        subtitle = request.form.get('subtitle')
        text = request.form.get('text')
        
        new_card = Card(title=title, subtitle=subtitle, text=text, user_id=current_user.id)
        db.session.add(new_card)
        db.session.commit()
        
        flash('Card created successfully!', 'success')
        return redirect(url_for('index'))
    
    return redirect(url_for('create'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)