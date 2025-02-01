# Chat Assistant for SQLite Database

## Overview

A Python-based chat assistant that queries an SQLite database to provide information about employees and departments. Supports natural language queries and returns structured answers.

## Features

- **Supported Queries**:
  - Show all employees in the [department].
  - Who is the manager of the [department]?
  - List employees hired after [date].
  - Total salary expense for the [department].

- **Error Handling**: Gracefully handles invalid queries, missing records, and incorrect input formats.

## Database Schema

### Employees Table:
- `ID`, `Name`, `Department`, `Salary`, `Hire_Date`

### Departments Table:
- `ID`, `Name`, `Manager`

## Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/your-username/chat-assistant-sqlite.git
   cd chat-assistant-sqlite
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```
   python app.py
   ```
   Access at http://127.0.0.1:5000/.

 ## Example Query

### POST request to `/chat`:

```json
{
  "query": "show me all employees in the Sales department"
}
```
## Example Response:

```json
{
  "response": "Sales Department Employees: Arjun, Kavita"
}
```
     
