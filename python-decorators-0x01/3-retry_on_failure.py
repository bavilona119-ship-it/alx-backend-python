#!/usr/bin/python3
"""
3-retry_on_failure.py

Decorators for database connection handling and retrying queries.
"""

import sqlite3
import functools
import time


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


def retry_on_failure(retries=3, delay=2):
    """
    Retry a function if it raises an exception.
    - retries: how many times to retry
    - delay: wait time (seconds) between retries
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    print(f"Attempt {attempts} failed: {e}")
                    if attempts < retries:
                        print(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        print("All retries failed ❌")
                        raise
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    """
    Example query: fetch all users.
    Will retry automatically if it fails.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


if __name__ == "__main__":
    users = fetch_users_with_retry()
    print("Fetched users:", users)
