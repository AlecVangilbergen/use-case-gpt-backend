from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import User as UserSchema, UserBase, UserCreate, UserOut

class UserService():
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def get_users(self) -> list[UserOut]:
        return await self.user_repo.get_users()

    async def get_user_by_email(self, email: str) -> UserSchema:
        return await self.user_repo.get_user_by_email(email)
    
    async def get_user_by_id(self, user_id: int) -> UserOut:
        return await self.user_repo.get_user_by_id(user_id)
    
    async def create_user(self, user: UserCreate):
        return await self.user_repo.create_user(user)
    
    async def get_prompt_by_id(self, user_id: int) -> str:
        return await self.user_repo.get_prompt_by_id(user_id)
    