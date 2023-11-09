from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.models import User
from sqlalchemy.engine import Result
from .schemas import UserCreateSchema, UserSchema, UserUpdateSchema


async def get_users(session: AsyncSession) -> list[User]:
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    return await session.scalar(stmt)


async def add_user(session: AsyncSession, user: UserCreateSchema):
    user = user.model_dump()
    user["hash_password"] = user["password"]  # todo password hashing
    del user["password"]
    db_user = User(**user)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


async def update_user_partition(
    session: AsyncSession,
    user_id: int,
    new_user: UserUpdateSchema,
):
    user = await get_user_by_id(user_id=user_id, session=session)
    for name, value in new_user.model_dump(exclude_unset=True).items():
        if name == "password":
            name = "hash_password"
        setattr(user, name, value)

    await session.commit()
    await session.refresh(user)
    return user


async def delete_user(session: AsyncSession, user: User):
    await session.delete(user)
    await session.commit()
