from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app) #I have added this to encrypting the Password of user and storing in Db
login_manager = LoginManager()
login_manager.init_app(app)

# Creting 2 tables/models for storing data
# Chef Model
class Chef(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    mobile_number = db.Column(db.String(20))

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

# Recipe Model
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('chef.id'), nullable=False)
    chef = db.relationship('Chef', backref=db.backref('recipes'))

@login_manager.user_loader
def load_user(user_id):
    return Chef.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        mobile_number = request.form['mobile_number']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = Chef(username=username, password=hashed_password, name=name, mobile_number=mobile_number)
        db.session.add(new_user)
        db.session.commit()
        flash('Registered successfully. Please log in.', 'success')
        return redirect(url_for('login'))
    # if found GET call for this API
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Chef.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/recipes')
@login_required
def recipes():
    recipes = Recipe.query.all()
    return render_template('recipes.html', recipes=recipes)

@app.route('/add_recipe', methods=['GET', 'POST'])
@login_required
def add_recipe():
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        description = request.form['description']
        new_recipe = Recipe(title=title, ingredients=ingredients, instructions=instructions, description=description, created_by=current_user.id)
        db.session.add(new_recipe)
        db.session.commit()
        flash('Recipe added successfully.', 'success')
        return redirect(url_for('recipes'))
    return render_template('add_recipe.html')

@app.route('/recipe/<int:recipe_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if current_user.id != recipe.created_by:
        flash('You are not authorized to edit this recipe.', 'error')
        return redirect(url_for('recipes'))
    if request.method == 'POST':
        recipe.title = request.form['title']
        recipe.ingredients = request.form['ingredients']
        recipe.instructions = request.form['instructions']
        recipe.description = request.form['description']
        db.session.commit()
        flash('Recipe updated successfully.', 'success')
        return redirect(url_for('recipes'))
    return render_template('edit_recipe.html', recipe=recipe)

@app.route('/recipe/<int:recipe_id>/delete', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if current_user.id != recipe.created_by:
        flash('You are not authorized to delete this recipe.', 'error')
        return redirect(url_for('recipes'))
    db.session.delete(recipe)
    db.session.commit()
    flash('Recipe deleted successfully.', 'success')
    return redirect(url_for('recipes'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
