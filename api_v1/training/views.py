from typing import Annotated, TYPE_CHECKING
import random
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from . import train_generator
from core.database import db_helper
from core.database.models import User
from api_v1.user import get_current_user
from . import crud
from .scemas import SAnswer

if TYPE_CHECKING:
    from core.providers.Dictionary.schemas import SSenseP

router = APIRouter(prefix="/training", tags=["training"])


@router.get(
    "/",
    summary="Get training",
)
async def get_training(
    number: Annotated[int, Query(ge=1)],
    user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    await train_generator.define_mastered_senses(session, user)
    bunch_train_content: list[SSenseP] = await train_generator.generate(session, user, number)
    random.shuffle(bunch_train_content)
    return bunch_train_content


@router.post(
    "/",
    summary="Add answer",
)
async def get_training(
    answer: SAnswer,
    user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.add_answer(session, user, answer)
