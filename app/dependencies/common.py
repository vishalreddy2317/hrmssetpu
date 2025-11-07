# from typing import Generator
# from fastapi import Depends, HTTPException, status
# from sqlalchemy.ext.asyncio import AsyncSession
# from app.core.database import get_db_session
# from app.models.user import User
# from app.core.security import verify_token as decode_access_token

# # ✅ Dependency to get DB session
# async def get_db() -> Generator[AsyncSession, None, None]:
#     async with get_db_session() as session:
#         yield session

# # ✅ Dependency to get current authenticated user
# async def get_current_user(token: str = Depends(decode_access_token), db: AsyncSession = Depends(get_db)) -> User:
#     if not token:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
#     return token

# # ✅ Role-based access control
# def require_roles(*roles: str):
#     async def role_checker(current_user: User = Depends(get_current_user)):
#         if current_user.role.name not in roles:
#             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden: insufficient role")
#         return current_user
#     return role_checker
from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session
from app.models.user import User
from app.core.security import verify_token as decode_access_token

# ✅ Correct async dependency
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_db_session():
        yield session

# ✅ Current authenticated user
async def get_current_user(
    token: str = Depends(decode_access_token),
    db: AsyncSession = Depends(get_db)
) -> User:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return token

# ✅ Role-based access control
def require_roles(*roles: str):
    async def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role.name not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access forbidden: insufficient role"
            )
        return current_user
    return role_checker
