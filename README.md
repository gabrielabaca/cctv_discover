# CCTV DISCOVER

Brief project description.

## About the Author

This project is developed by [Gabriel Abaca](https://www.linkedin.com/in/luciogabrielabaca/). 

Feel free to connect with me on LinkedIn for any questions or collaboration opportunities.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/gabrielabaca/cctv_discover.git
```

2. Navigate to the project directory:
```bash
cd your-project
```

3. Create and activate a virtual environment (optional but recommended):
```bash
python3 -m venv venv
source venv/bin/activate
```

4. Install the project dependencies:
```bash
pip install -r requirements.txt
```

5. Set up environment variables:
* Copy the .env_example file located in the envs/ directory to the project root directory.
* Rename the copied file to .env.
* Edit the .env file and configure the necessary variables, such as database connection keys.

## Database
This project uses a PostgreSQL database. Make sure you have PostgreSQL installed and properly configured.

1. Create a new database in PostgreSQL.

2. Update the database configuration in the .env file of the project with the credentials and details of your newly created database.

## Database Migrations
To migrate the database, use Django Admin and run the following commands:

```bash
python manage.py makemigrations
python manage.py migrate
```

This will create and apply the necessary migrations to your database.

## Running the Development Server
To run the Django development server, use the following command:
```bash 
python manage.py runserver
```

The server will run at http://localhost:8000/ by default.