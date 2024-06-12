# Chef Registration and Recipe Creation Web Application

This web application allows chefs to register, login, create recipes, view their recipes, edit and delete too.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/shivam0906/volgainfotech_pythnproject/
    ```
2. Navigate to the project directory:

    ```bash
    cd chef-registration-recipe-creation
    ```

3. Create a virtual environment (optional but recommended):

    ```bash
    python3 -m venv venv
    ```

4. Activate the virtual environment:

    ```bash
    venv\Scripts\activate
    ```

5. Install the required libraries:

    ```bash
    pip install -r requirements.txt
    ```

## Database Setup

1. The application uses SQLite as the database, so no additional setup is required for the database.

2. Run the following commands to create the initial database schema:

    ```bash
    python
    from app import db
    db.create_all()
    exit()
    ```

## Running the Application

1. Ensure you are in the project directory and the virtual environment is activated.

2. Run the Flask application:

    ```bash
    flask run
    ```

3. Open a web browser and navigate to `http://127.0.0.1:5000/` to access the application.

## Usage

1. Register a new account by clicking on the "Register" link and filling out the registration form.
2. Login with your registered username and password.
3. Once logged in, you can:
   - Add a new recipe by clicking on the "Add Recipe" link and filling out the recipe form.
   - View the list of all recipes by clicking on the "Recipes" link.
   - Edit or delete your own recipes by clicking on the corresponding links next to each recipe.
   - Logout from your account by clicking on the "Logout" link

## Running Tests

To run the tests, execute the following command:

```bash
python -m unittest
