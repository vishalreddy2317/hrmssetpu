"""
✅ Database migration script - FIXED async/sync issues
"""
import asyncio
from app.db.session import init_db


async def create_tables():
    """Create all database tables"""
    try:
        await init_db()
        print("✅ Database tables created successfully!")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")


if __name__ == "__main__":
    asyncio.run(create_tables())