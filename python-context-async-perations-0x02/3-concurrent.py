#!/usr/bin/python3
"""
3-concurrent.py

Run multiple database queries concurrently using asyncio.gather and aiosqlite.
"""

import asyncio
import aiosqlite


async def async_fetch_users(db_name="users.db"):
    """Fetch all users asynchronously."""
    async with aiosqlite.connect(db_name) as db:
        cursor = await db.execute("SELECT * FROM users")
        rows = await cursor.fetchall()
        await cursor.close()
        return rows


async def async_fetch_older_users(db_name="users.db"):
    """Fetch users older than 40 asynchronously."""
    async with aiosqlite.connect(db_name) as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > ?", (40,))
        rows = await cursor.fetchall()
        await cursor.close()
        return rows


async def fetch_concurrently():
    """Run both queries concurrently."""
    results_all, results_older = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("✅ All users:")
    for row in results_all:
        print(row)

    print("\n✅ Users older than 40:")
    for row in results_older:
        print(row)


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
