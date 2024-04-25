import asyncio

import asyncpg

from config import (
    DB_HOST,
    DB_PORT,
    POSTGRES_DB,
    POSTGRES_PASSWORD,
    POSTGRES_USER
)


async def get_db_connection():
    return await asyncpg.connect(
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=POSTGRES_DB
    )


async def create_db():
    conn = await get_db_connection()
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS requests(
            id SERIAL PRIMARY KEY,
            user_id INTEGER,
            username VARCHAR,
            website VARCHAR,
            screenshot_path VARCHAR,
            execution_time REAL,
            date TIMESTAMP default now()
        );
    ''')
    await conn.close()


async def insert(request_info, screenshot_path, execution_time):
    conn = await get_db_connection()
    await conn.execute(
        '''INSERT INTO requests(user_id, username, website, screenshot_path, execution_time)
        VALUES($1, $2, $3, $4, $5);''',
        request_info['user_id'],
        request_info['username'],
        request_info['website'],
        screenshot_path,
        execution_time
    )
    await conn.close()


if __name__ == '__main__':
    asyncio.run(create_db())
