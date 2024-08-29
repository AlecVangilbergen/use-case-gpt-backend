from typing import List, Protocol, Optional
from app.models.user import User
from app.schemas.user import User as UserSchema, UserBase, UserCreate
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class InterfaceUserRepository(Protocol):
    async def get_user_by_email(self, email: str) -> Optional[UserSchema]:
        ...

    async def get_user_by_id(self, user_id: int) -> Optional[UserSchema]:
        ...

    async def create_user(self, user: UserSchema) -> UserSchema:
        ...

    async def update_user(self, user: UserSchema) -> UserSchema:
        ...

    async def delete_user(self, user_id: int) -> None:
        ...

class UserRepository(InterfaceUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def get_users(self) -> List[UserBase]:
        result = await self.session.execute(select(User))
        users = result.scalars().all()
        return [UserSchema.from_orm(user) for user in users]

    async def get_user_by_email(self, email: str) -> Optional[UserSchema]:
        result = await self.session.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        if user:
            return UserSchema.from_orm(user)
        return None

    async def get_user_by_id(self, user_id: int) -> Optional[UserSchema]:
        result = await self.session.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        if user:
            return UserSchema.from_orm(user)
        return None

    async def create_user(self, user: UserCreate) -> UserSchema:
        hashed_password = self.pwd_context.hash(user.password)
        new_user = User(email=user.email, hashed_password=hashed_password)
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return UserSchema.from_orm(new_user)
