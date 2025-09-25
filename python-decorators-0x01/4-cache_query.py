#!/usr/bin/python3
"""
4-cache_query.py

Decorator that caches database query results.
"""

import sqlite3
import functools

# Global cache dictionary
query_cache = {}


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


def cache_query(func):
    """
    Cache results of queries based on the SQL string.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract query argument (we assume it's passed as "query=")
        query = kwargs.get("query")
        if query in query_cache:
            print(f"Cache hit for query: {query}")
            return query_cache[query]

        print(f"Cache miss for query: {query}. Running query...")
        result = func(*args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """
    Execute a query with caching.
    """
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


if __name__ == "__main__":
    # First call: runs the query and caches it
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print("First call:", users)

    # Second call: fetches result from cache
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print("Second call (cached):", users_again)
