#!/usr/bin/env python3
"""
seed.py

Prototypes required by the assignment / 0-main.py:
- connect_db()
- create_database(connection)
- connect_to_prodev()
- create_table(connection)
- insert_data(connection, data)

Additional helper:
- stream_user_rows(connection)  <-- generator that yields rows one-by-one
"""

import os
import csv
import uuid
from typing import Optional, Iterator, Tuple
import mysql.connector
from mysql.connector import Error

# Defaults (can be overridden with environment variables)
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")  # often empty on local dev setups
DB_NAME = "ALX_prodev"
TABLE_NAME = "user_data"


def connect_db() -> Optional[mysql.connector.MySQLConnection]:
    """
    Connect to MySQL server (no database specified).
    Returns a mysql.connector connection or None on failure.
    """
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            autocommit=False
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"connect_db error: {e}")
    return None


def create_database(connection: mysql.connector.MySQLConnection) -> None:
    """Create database ALX_prodev if it does not exist."""
    try:
        cur = connection.cursor()
        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`;")
        connection.commit()
        cur.close()
    except Error as e:
        print(f"create_database error: {e}")


def connect_to_prodev() -> Optional[mysql.connector.MySQLConnection]:
    """
    Connect to the ALX_prodev database.
    Returns the connection or None on error.
    """
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            autocommit=False
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"connect_to_prodev error: {e}")
    return None


def create_table(connection: mysql.connector.MySQLConnection) -> None:
    """
    Create the user_data table if it does not exist with the required fields:
    user_id (CHAR(36) UUID) PRIMARY KEY, name VARCHAR NOT NULL, email VARCHAR NOT NULL, age DECIMAL NOT NULL
    Also creates an index on user_id (primary key is already indexed but we include an explicit index per spec).
    """
    try:
        cur = connection.cursor()
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS `{TABLE_NAME}` (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(5,0) NOT NULL
            );
        """)
        # explicit index (redundant for primary key but included to match "Indexed" requirement)
        cur.execute(f"CREATE INDEX IF NOT EXISTS idx_user_id ON `{TABLE_NAME}` (user_id);")
        connection.commit()
        cur.close()
        print("Table user_data created successfully")
    except Error as e:
        print(f"create_table error: {e}")


def insert_data(connection: mysql.connector.MySQLConnection, data: str) -> None:
    """
    Insert rows from CSV file path `data` into the user_data table.
    - Accepts CSV with headers: at least (name, email, age). If user_id present it will be used; otherwise a UUID is generated.
    - Skips rows that already exist (by user_id OR email).
    """
    try:
        cur = connection.cursor()
        csv_file = data
        with open(csv_file, newline='', encoding='utf-8') as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                # read values (tolerant to different header names)
                user_id = row.get('user_id') or row.get('id') or ''
                if not user_id:
                    user_id = str(uuid.uuid4())

                name = row.get('name') or row.get('full_name') or ''
                email = row.get('email') or ''
                age_raw = row.get('age') or row.get('Age') or 0

                # coerce age to integer-like value for DECIMAL(5,0)
                try:
                    age = int(float(age_raw))
                except Exception:
                    age = 0

                # avoid duplicate insertion (by user_id or email)
                cur.execute(
                    f"SELECT 1 FROM `{TABLE_NAME}` WHERE user_id = %s OR email = %s LIMIT 1;",
                    (user_id, email)
                )
                if cur.fetchone():
                    # already present, skip
                    continue

                cur.execute(
                    f"INSERT INTO `{TABLE_NAME}` (user_id, name, email, age) VALUES (%s, %s, %s, %s);",
                    (user_id, name, email, age)
                )

        connection.commit()
        cur.close()
        # lightweight feedback (keeps behaviour readable)
        print("Data inserted (or skipped when duplicate).")
    except FileNotFoundError:
        print(f"insert_data error: CSV file not found: {data}")
    except Error as e:
        print(f"insert_data error: {e}")


def stream_user_rows(connection: mysql.connector.MySQLConnection) -> Iterator[Tuple]:
    """
    Generator that streams rows from user_data one by one.
    Yields tuples in the same order as SELECT (user_id, name, email, age).
    Example usage:
        for row in stream_user_rows(conn):
            print(row)
    """
    try:
        # unbuffered cursor allows row-by-row consumption (reduces memory for large result sets)
        cur = connection.cursor(buffered=False)
        cur.execute(f"SELECT user_id, name, email, age FROM `{TABLE_NAME}`;")
        # fetch one at a time
        row = cur.fetchone()
        while row is not None:
            yield row
            row = cur.fetchone()
        cur.close()
    except Error as e:
        print(f"stream_user_rows error: {e}")
        return


# optional: if run directly, a small demo (won't run when imported by 0-main.py)
if __name__ == "__main__":
    conn = connect_db()
    if not conn:
        print("Could not connect to MySQL server. Check credentials and that MySQL is running.")
        raise SystemExit(1)

    create_database(conn)
    conn.close()

    conn2 = connect_to_prodev()
    if not conn2:
        print("Could not connect to ALX_prodev database.")
        raise SystemExit(1)

    create_table(conn2)
    # try to insert if a user_data.csv exists in same directory
    csv_path = os.path.join(os.path.dirname(__file__), "user_data.csv")
    insert_data(conn2, csv_path)

    # demo streaming (prints first 3 rows)
    i = 0
    for r in stream_user_rows(conn2):
        print(r)
        i += 1
        if i >= 3:
            break

    conn2.close()
