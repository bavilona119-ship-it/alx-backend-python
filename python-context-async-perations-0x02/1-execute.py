#!/usr/bin/python3
"""
1-execute.py

Reusable query context manager that executes a query
and returns the results automatically.
"""

import sqlite3


class ExecuteQuery:
    """
    Context manager that:
    - Opens a database connection
    - Executes a given query with parameters
    - Returns the results
    - Closes the connection automatically
    """

    def __init__(self, query, params=None, db_name="users.db"):
        self.db_name = db_name
        self.query = query
        self.params = params or []
        self.conn = None
        self.results = None

    def __enter__(self):
        """Open DB connection, execute query, return results."""
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
        cursor.execute(self.query, self.params)
        self.results = cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close DB connection automatically when exiting context."""
        if self.conn:
            self.conn.close()
        # Do not suppress exceptions
        return False


if __name__ == "__main__":
    # Example usage
    query = "SELECT * FROM users WHERE age > ?"
    param = (25,)  # tuple with one parameter

    with ExecuteQuery(query, param) as results:
        print("Users older than 25:")
        for row in results:
            print(row)

