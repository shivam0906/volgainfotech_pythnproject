from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

app = Flask(_name_)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

class Chef(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    mobile_number = db.Column(db.String(20), nullable=False)
    recipes = db.relationship('Recipe', backref='chef', lazy=True)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    instructions = db.Column(db.Text, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('chef.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return Chef.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        full_name = request.form['full_name']
        mobile_number = request.form['mobile_number']
        new_chef = Chef(username=username, password=password, full_name=full_name, mobile_number=mobile_number)
        db.session.add(new_chef)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        chef = Chef.query.filter_by(username=username).first()
        if chef and chef.password == password:
            login_user(chef)
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    chef = Chef.query.get(current_user.id)
    recipes = chef.recipes
    return render_template('dashboard.html', chef=chef, recipes=recipes)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/recipe/create', methods=['GET', 'POST'])
@login_required
def create_recipe():
    if request.method == 'POST':
        instructions = request.form['instructions']
        title = request.form['title']
        description = request.form['description']
        ingredients = request.form['ingredients']
        new_recipe = Recipe(instructions=instructions, title=title, description=description, ingredients=ingredients, created_by=current_user.id)
        db.session.add(new_recipe)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('create_recipe.html')

if _name_ == '_main_':
    db.create_all()
    app.run(debug=True)