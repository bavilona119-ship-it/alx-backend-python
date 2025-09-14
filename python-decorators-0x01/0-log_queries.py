 #!/usr/bin/python3
"""
0-log_queries.py

Implements log_queries decorator that logs function calls
with timestamp and function name.
"""

from datetime import datetime
from functools import wraps


def log_queries(func):
    """Decorator to log query executions with timestamp."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Log before executing
        print(f"[{datetime.now()}] Executing {func.__name__}")
        result = func(*args, **kwargs)
        # Optionally log after execution
        print(f"[{datetime.now()}] Finished {func.__name__}")
        return result
    return wrapper


# Example usage
if __name__ == "__main__":
    @log_queries
    def sample_query(x, y):
        return x + y

    print("Result:", sample_query(3, 5))

