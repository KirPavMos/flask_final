from flask import Flask, render_template,request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)



@login_manager.user_loader
def load_user(user_id):
    return db.session.query(Users).get(user_id)

@app.route('/register', methods=["GET", "POST"])
def register():
   
 
@app.route("/login/", methods=["GET", "POST"])
def login():

  \

@app.route('/logout/')
@login_required
def logout():
  
@app.route('/')
def index():

@app.route('/home')
def home():

@app.route('/card/<int:id>')
@login_required
def card(id):

@app.route('/create')
@login_required
def create():

@app.route('/form_create', methods=['GET','POST'])
@login_required
def form_create():

if __name__ == "__main__":
    app.secret_key = 'lol'
    app.run(debug=True)