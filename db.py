import aiosqlite

DB_PATH = "db.sqlite3"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS user_timezones (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                timezone TEXT
            )
        """)
        await db.commit()

async def set_timezone(user_id: int, username: str, tz: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO user_timezones (user_id, username, timezone)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
            username=excluded.username,
            timezone=excluded.timezone
        """, (user_id, username, tz))
        await db.commit()

async def get_timezone(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT timezone FROM user_timezones WHERE user_id = ?", (user_id,)) as cur:
            row = await cur.fetchone()
            return row[0] if row else None

async def get_all_timezones():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT user_id, username, timezone FROM user_timezones") as cur:
            return await cur.fetchall()
