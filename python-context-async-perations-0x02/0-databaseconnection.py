#!/usr/bin/python3
"""
0-databaseconnection.py

Custom class-based context manager for database connections.
"""

import sqlite3


class DatabaseConnection:
    """
    Context manager for handling SQLite database connections.
    Automatically opens and closes the connection.
    """

    def __init__(self, db_name="users.db"):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """Open the database connection when entering the context."""
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Close the database connection when exiting the context.
        exc_type, exc_val, exc_tb are used to handle exceptions.
        """
        if self.conn:
            self.conn.close()
        # Returning False means exceptions (if any) are not suppressed
        return False


if __name__ == "__main__":
    # Example usage of the context manager
    with DatabaseConnection("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        print("Users from database:")
        for row in rows:
            print(row)
