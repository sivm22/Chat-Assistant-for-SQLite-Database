import sqlite3
import os
import logging
import re
from datetime import datetime
from flask import Flask, request, jsonify

# Flask App Initialization
app = Flask(__name__)

# Database Configuration
DATABASE = "COMPANY.db"

# Logging Configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def create_database():
    """Create the SQLite database if it doesn't exist."""
    if not os.path.exists(DATABASE):
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()

            # Create Employees Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Employees (
                    ID INTEGER PRIMARY KEY,
                    Name TEXT NOT NULL,
                    Department TEXT NOT NULL,
                    Salary INTEGER NOT NULL,
                    Hire_Date TEXT NOT NULL
                )
            ''')

            # Create Departments Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Departments (
                    ID INTEGER PRIMARY KEY,
                    Name TEXT NOT NULL,
                    Manager TEXT NOT NULL
                )
            ''')

            # Insert Sample Data
            cursor.executemany('INSERT INTO Employees VALUES (?, ?, ?, ?, ?)', [
                (1, 'Arjun', 'Sales', 50000, '2021-01-15'),
                (2, 'Ravi', 'Engineering', 70000, '2020-06-10'),
                (3, 'Sunita', 'Marketing', 60000, '2022-03-20')
            ])

            cursor.executemany('INSERT INTO Departments VALUES (?, ?, ?)', [
                (1, 'Sales', 'Arjun'),
                (2, 'Engineering', 'Ravi'),
                (3, 'Marketing', 'Sunita')
            ])

            conn.commit()


# Ensure the database is created when the app starts
create_database()


def query_database(query, params=(), fetch_one=False):
    """Helper function to query the database with proper error handling."""
    try:
        with sqlite3.connect(DATABASE) as conn:
            conn.row_factory = sqlite3.Row  # Return results as dictionaries
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone() if fetch_one else cursor.fetchall()
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
        return None


def validate_date(date_str):
    """Ensure date format is YYYY-MM-DD."""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


@app.after_request
def add_cors_headers(response):
    """Allow cross-origin requests if needed."""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


@app.route('/')
def home():
    """Home route to prevent 404 errors on root access."""
    return jsonify({"message": "Welcome to the Employee Chat API! Use POST /chat to interact."})


@app.route('/favicon.ico')
def favicon():
    """Handle favicon.ico requests to prevent unnecessary errors."""
    return '', 204  # Respond with "No Content"


@app.route('/chat', methods=['POST'])
def chat():
    """Process user queries related to employees and departments."""
    user_input = request.json.get('query', '').strip().lower()
    response = {"response": "", "error": None}

    try:
        # Extract query parameters from brackets [ ]
        match = re.search(r"\[(.*?)\]", user_input)
        if not match:
            raise ValueError("Please specify parameters in [brackets]")

        param = match.group(1).strip()

        # Handling different queries
        if "show me all employees in the" in user_input:
            result = query_database("SELECT Name FROM Employees WHERE LOWER(Department) = LOWER(?)", (param,))
            response["response"] = format_employees(result, param)

        elif "who is the manager of the" in user_input:
            result = query_database("SELECT Manager FROM Departments WHERE LOWER(Name) = LOWER(?)", (param,), fetch_one=True)
            response["response"] = format_manager(result, param)

        elif "list all employees hired after" in user_input:
            if not validate_date(param):
                raise ValueError("Invalid date format. Use YYYY-MM-DD")
            result = query_database("SELECT Name FROM Employees WHERE Hire_Date > ?", (param,))
            response["response"] = format_hired_after(result, param)

        elif "total salary expense for the" in user_input:
            result = query_database("SELECT SUM(Salary) AS total FROM Employees WHERE LOWER(Department) = LOWER(?)", (param,), fetch_one=True)
            response["response"] = format_salary_expense(result, param)

        else:
            response["response"] = "I can assist with employee lists, manager info, hiring dates, and salary expenses. Try rephrasing!"

    except Exception as e:
        response["response"] = "Sorry, I encountered an error processing your request."
        response["error"] = str(e)
        logging.error(f"Error processing request: {e}")

    return jsonify(response)


# 📌 Response Formatting Functions
def format_employees(result, department):
    if not result:
        return f"No employees found in the {department.title()} department."
    names = [row['Name'] for row in result]
    return f"{department.title()} Department Employees: {', '.join(names)}"


def format_manager(result, department):
    if not result or not result['Manager']:
        return f"No manager found for the {department.title()} department."
    return f"Manager of {department.title()}: {result['Manager']}"


def format_hired_after(result, date):
    if not result:
        return f"No employees hired after {date}."
    names = [row['Name'] for row in result]
    return f"Employees hired after {date}: {', '.join(names)}"


def format_salary_expense(result, department):
    if not result or result['total'] is None:
        return f"No salary data available for the {department.title()} department."
    return f"Total {department.title()} Salary Expense: ₹{result['total']:,}"


if __name__ == '__main__':
    # Run Flask app, disable reloader
    app.run(debug=True, port=5000, use_reloader=False)
