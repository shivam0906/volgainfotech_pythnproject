# Chef Registration and Recipe Creation Web Application

This web application allows chefs to register, login, create recipes, and view their dashboard.

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

1. Register as a new chef by clicking on the "Register" link on the home page.

2. After registration, login with your credentials.

3. Once logged in, you can create recipes by clicking on the "Create Recipe" link in the dashboard.

4. You can view your created recipes in the dashboard.

5. Logout from the application by clicking on the "Logout" link in the dashboard.
