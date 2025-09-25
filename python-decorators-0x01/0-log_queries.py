#!/usr/bin/python3
"""
0-log_queries.py

Implements log_queries decorator that logs function calls
with timestamp and function name.
"""

from datetime import datetime
from functools import wraps
import mysql.connector
from mysql.connector import Error


def log_queries(func):
    """Decorator to log query executions with timestamp."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[{datetime.now()}] Executing {func.__name__}")
        result = func(*args, **kwargs)
        print(f"[{datetime.now()}] Finished {func.__name__}")
        return result
    return wrapper


@log_queries
def connect():
    """Connect to MySQL server (test function)."""
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",         # adjust if needed
            password="root"      # adjust if needed
        )
        if connection.is_connected():
            print("Connection successful")
            connection.close()
    except Error as e:
        print(f"Error while connecting: {e}")


if __name__ == "__main__":
    connect()
