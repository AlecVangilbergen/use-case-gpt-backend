from sqlalchemy import select
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import User as UserSchema, UserBase, UserCreate

class AuthRepository():

    async def get_user_by_email(self, db: AsyncSession, email: str) -> UserSchema:
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        if user:
            return UserSchema.from_orm(user)
        return None