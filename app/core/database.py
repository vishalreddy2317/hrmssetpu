"""
PostgreSQL Database Configuration using SQLAlchemy 2.0
Supports both sync and async operations
"""

from typing import Generator, AsyncGenerator
from sqlalchemy import (
    create_engine,
    event,
    pool,
    text,
)
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.orm import (
    sessionmaker,
    Session,
    DeclarativeBase,
    declared_attr,
)
from sqlalchemy.pool import NullPool, QueuePool
from contextlib import contextmanager, asynccontextmanager
import logging
from datetime import datetime

from .config import settings


# Configure logging
logger = logging.getLogger(__name__)


# ============================================
# SQLAlchemy 2.0 Declarative Base
# ============================================

class Base(DeclarativeBase):
    """
    Base class for all models using SQLAlchemy 2.0
    """
    
    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Generate table name automatically from class name"""
        return cls.__name__.lower() + 's'
    
    def dict(self):
        """Convert model to dictionary"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
    
    def __repr__(self):
        """String representation"""
        attrs = ", ".join(
            f"{col.name}={getattr(self, col.name)}"
            for col in self.__table__.columns
        )
        return f"<{self.__class__.__name__}({attrs})>"


# ============================================
# Synchronous Database Engine
# ============================================

# Create synchronous engine
engine = create_engine(
    settings.database_url,
    echo=settings.database.echo,
    echo_pool=settings.database.echo_pool,
    pool_size=settings.database.pool_size,
    max_overflow=settings.database.max_overflow,
    pool_timeout=settings.database.pool_timeout,
    pool_recycle=settings.database.pool_recycle,
    pool_pre_ping=settings.database.pool_pre_ping,
    poolclass=QueuePool,
    connect_args={
        "options": f"-c statement_timeout={settings.database.statement_timeout}",
        "connect_timeout": 10,
    },
    future=True,  # SQLAlchemy 2.0 style
)


# Create session factory
SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


# ============================================
# Asynchronous Database Engine
# ============================================

# Create async engine
async_engine = create_async_engine(
    settings.async_database_url,
    echo=settings.database.echo,
    pool_size=settings.database.pool_size,
    max_overflow=settings.database.max_overflow,
    pool_timeout=settings.database.pool_timeout,
    pool_recycle=settings.database.pool_recycle,
    pool_pre_ping=settings.database.pool_pre_ping,
    future=True,
)


# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


# ============================================
# Database Event Listeners
# ============================================

@event.listens_for(engine, "connect")
def set_postgresql_pragmas(dbapi_conn, connection_record):
    """Set PostgreSQL connection parameters"""
    cursor = dbapi_conn.cursor()
    
    # Set timezone
    cursor.execute("SET TIME ZONE 'UTC'")
    
    # Set search path
    cursor.execute(f"SET search_path TO {settings.database.schema}, public")
    
    # Enable query logging in development
    if settings.is_development:
        cursor.execute("SET log_statement = 'all'")
    
    cursor.close()


@event.listens_for(engine, "checkout")
def receive_checkout(dbapi_conn, connection_record, connection_proxy):
    """Handle connection checkout from pool"""
    logger.debug("Connection checked out from pool")


@event.listens_for(engine, "checkin")
def receive_checkin(dbapi_conn, connection_record):
    """Handle connection checkin to pool"""
    logger.debug("Connection returned to pool")


# ============================================
# Session Dependencies
# ============================================

def get_db() -> Generator[Session, None, None]:
    """
    Dependency for getting synchronous database session
    Usage in FastAPI:
        @router.get("/items")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Database session error: {str(e)}")
        raise
    finally:
        db.close()


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting asynchronous database session
    Usage in FastAPI:
        @router.get("/items")
        async def get_items(db: AsyncSession = Depends(get_async_db)):
            result = await db.execute(select(Item))
            return result.scalars().all()
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Async database session error: {str(e)}")
            raise
        finally:
            await session.close()


# ============================================
# Context Managers
# ============================================

@contextmanager
def get_db_context():
    """
    Context manager for database session
    Usage:
        with get_db_context() as db:
            db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Database context error: {str(e)}")
        raise
    finally:
        db.close()


@asynccontextmanager
async def get_async_db_context():
    """
    Async context manager for database session
    Usage:
        async with get_async_db_context() as db:
            await db.execute(select(User))
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Async database context error: {str(e)}")
            raise
        finally:
            await session.close()


# ============================================
# Database Utility Functions
# ============================================

def check_db_connection() -> bool:
    """
    Check if database connection is working
    Returns: True if connection successful, False otherwise
    """
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            logger.info("✅ PostgreSQL connection successful!")
            return True
    except Exception as e:
        logger.error(f"❌ PostgreSQL connection failed: {str(e)}")
        return False


async def check_async_db_connection() -> bool:
    """
    Check if async database connection is working
    Returns: True if connection successful, False otherwise
    """
    try:
        async with async_engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
            logger.info("✅ Async PostgreSQL connection successful!")
            return True
    except Exception as e:
        logger.error(f"❌ Async PostgreSQL connection failed: {str(e)}")
        return False


def create_all_tables():
    """
    Create all database tables
    WARNING: Only use in development!
    """
    logger.info("Creating all database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("✅ All tables created successfully!")


def drop_all_tables():
    """
    Drop all database tables
    WARNING: This will delete all data!
    """
    logger.warning("⚠️  Dropping all database tables...")
    Base.metadata.drop_all(bind=engine)
    logger.info("✅ All tables dropped!")


async def create_all_tables_async():
    """
    Create all tables asynchronously
    """
    logger.info("Creating all database tables (async)...")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("✅ All tables created successfully (async)!")


def get_db_info() -> dict:
    """
    Get database connection information
    """
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT 
                current_database() as database,
                current_schema() as schema,
                version() as version,
                pg_size_pretty(pg_database_size(current_database())) as size
        """))
        row = result.fetchone()
        
        return {
            "database": row[0],
            "schema": row[1],
            "version": row[2],
            "size": row[3],
            "pool_size": settings.database.pool_size,
            "max_overflow": settings.database.max_overflow,
        }


def get_table_info() -> list:
    """
    Get information about all tables
    """
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT 
                schemaname,
                tablename,
                pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size,
                n_live_tup as row_count
            FROM pg_stat_user_tables
            ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
        """))
        
        return [
            {
                "schema": row[0],
                "table": row[1],
                "size": row[2],
                "rows": row[3],
            }
            for row in result
        ]


def vacuum_database():
    """
    Run VACUUM ANALYZE on database (PostgreSQL maintenance)
    """
    logger.info("Running VACUUM ANALYZE...")
    with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
        conn.execute(text("VACUUM ANALYZE"))
    logger.info("✅ VACUUM ANALYZE completed!")


def backup_database(backup_path: str) -> bool:
    """
    Create database backup using pg_dump
    Note: Requires pg_dump to be installed
    """
    import subprocess
    
    try:
        command = [
            "pg_dump",
            "-h", settings.database.host,
            "-p", str(settings.database.port),
            "-U", settings.database.user,
            "-F", "c",  # Custom format
            "-b",  # Include blobs
            "-v",  # Verbose
            "-f", backup_path,
            settings.database.name,
        ]
        
        logger.info(f"Creating database backup: {backup_path}")
        subprocess.run(command, check=True, env={"PGPASSWORD": settings.database.password})
        logger.info("✅ Database backup created successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Database backup failed: {str(e)}")
        return False


# ============================================
# Initialize Database
# ============================================

def init_db():
    """
    Initialize database on application startup
    """
    logger.info("Initializing database...")
    
    # Check connection
    if not check_db_connection():
        raise Exception("Failed to connect to PostgreSQL database")
    
    # Log database info
    db_info = get_db_info()
    logger.info(f"Connected to: {db_info['database']} ({db_info['version']})")
    logger.info(f"Database size: {db_info['size']}")
    
    # Create tables in development
    if settings.is_development:
        logger.info("Development mode: Creating tables if not exist...")
        create_all_tables()
    
    logger.info("✅ Database initialized successfully!")


# ============================================
# Exports
# ============================================

__all__ = [
    "Base",
    "engine",
    "async_engine",
    "SessionLocal",
    "AsyncSessionLocal",
    "get_db",
    "get_async_db",
    "get_db_context",
    "get_async_db_context",
    "check_db_connection",
    "check_async_db_connection",
    "create_all_tables",
    "drop_all_tables",
    "init_db",
    "get_db_info",
    "get_table_info",
    "vacuum_database",
    "backup_database",
]