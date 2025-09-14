#!/usr/bin/python3
"""
1-with_db_connection.py

A beginner-friendly example of using a decorator to manage database connections.
"""

import sqlite3
import functools


def with_db_connection(func):
    """
    A decorator that:
    - Opens a connection to 'users.db'
    - Passes the connection to the decorated function
    - Closes the connection automatically afterwards
    """
    @functools.wraps(func)  # preserves function name and docstring
    def wrapper(*args, **kwargs):
        # Step 1: Open the connection
        conn = sqlite3.connect("users.db")
        try:
            # Step 2: Call the function, but pass in 'conn' as the first argument
            result = func(conn, *args, **kwargs)
            return result
        finally:
            # Step 3: Always close the connection, even if there's an error
            conn.close()
    return wrapper


@with_db_connection
def get_user_by_id(conn, user_id):
    """
    Example function: fetch a user row from 'users' table using their ID.
    The 'conn' argument is injected automatically by the decorator.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


if __name__ == "__main__":
    # Example usage (make sure you have a users.db with a users table)
    user = get_user_by_id(user_id=1)
    print(user)

