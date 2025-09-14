#!/usr/bin/python3
"""
2-transactional.py

Decorators for automatic database connection handling
and transaction management.
"""

import sqlite3
import functools


def with_db_connection(func):
    """
    Opens a connection to 'users.db',
    passes it to the function,
    and closes it afterwards.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper


def transactional(func):
    """
    Wraps a function in a database transaction.
    - Commits if no error occurs.
    - Rolls back if an exception happens.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()   # success → save changes
            return result
        except Exception as e:
            conn.rollback()  # failure → undo changes
            print(f"Transaction failed: {e}")
            raise
    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """
    Update a user's email safely inside a transaction.
    """
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET email = ? WHERE id = ?",
        (new_email, user_id)
    )


if __name__ == "__main__":
    # Example usage
    update_user_email(user_id=1, new_email="Crawford_Cartwright@hotmail.com")
    print("User email updated successfully ✅")

