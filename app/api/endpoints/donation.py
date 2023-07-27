from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationAll, DonationCreate, DonationDB
from app.services.invest import worker


router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    response_model_exclude={'user_id'},
)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Только для зарегистрированных пользователей."""
    donation = await donation_crud.create(
        donation, session, user, pass_commit=True
    )
    session.add_all(
        worker(
            donation,
            await charity_project_crud.get_not_fully_invested(session)
        )
    )
    await session.commit()
    await session.refresh(donation)
    return donation


@router.get(
    '/',
    response_model=List[DonationAll],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    donations = await donation_crud.get_multi(session)
    return donations


@router.get(
    '/my',
    response_model=List[DonationDB],
    response_model_exclude={'user_id'}
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Получает список всех пожертвований для текущего пользователя."""
    donations = await donation_crud.get_by_user(session=session, user=user)
    return donations
