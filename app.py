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


create_database()
