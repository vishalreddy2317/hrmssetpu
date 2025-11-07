"""
✅ User repository - imports from auth.models
"""
from app.crud.user import user_crud
from app.auth.models import User  # ✅ Import from auth
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class UserRepository:
    def __init__(self):
        self.crud = user_crud

    async def get_by_email_or_phone(
        self, 
        db: AsyncSession, 
        email: str = None, 
        phone: str = None
    ):
        """Get user by email or phone"""
        stmt = select(User)
        if email:
            stmt = stmt.where(User.email == email)
        elif phone:
            stmt = stmt.where(User.phone == phone)
        else:
            return None
        
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_email(self, db: AsyncSession, email: str):
        """Get user by email"""
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    
    async def get_by_phone(self, db: AsyncSession, phone: str):
        """Get user by phone"""
        result = await db.execute(select(User).where(User.phone == phone))
        return result.scalar_one_or_none()
    
    async def get_by_username(self, db: AsyncSession, username: str):
        """Get user by username"""
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        """Get all users with pagination"""
        return await self.crud.get_all(db, skip=skip, limit=limit)


user_repository = UserRepository()