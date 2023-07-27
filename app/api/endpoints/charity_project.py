from datetime import datetime
from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_exists, check_charity_project_exists_for_update,
    check_charity_project_name_duplicate
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)
from app.services.invest import worker


FULL_INVESTED_ERROR = 'Закрытый проект нельзя редактировать!'
INVESTED_AMOUNT_ERROR = (
    'Нельзя устанавливать для проекта '
    'новую требуемую сумму меньше уже внесенной!'
)
CANT_CLOSE_OR_DELETE_ERROR = (
    'В проект были внесены средства, не подлежит удалению!'
)


router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_charity_project_name_duplicate(charity_project.name, session)
    charity_project = await charity_project_crud.create(
        charity_project, session, pass_commit=True
    )
    session.add_all(
        worker(
            charity_project,
            await donation_crud.get_not_fully_invested(session)
        )
    )
    await session.commit()
    await session.refresh(charity_project)
    return charity_project


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    charity_projects = await charity_project_crud.get_multi(session)
    return charity_projects


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
        charity_project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=FULL_INVESTED_ERROR
        )
    if (
        obj_in.full_amount and
        obj_in.full_amount < charity_project.invested_amount
    ):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=INVESTED_AMOUNT_ERROR
        )
    if obj_in.name:
        await check_charity_project_exists_for_update(
            obj_in, charity_project_id, session
        )
    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    if charity_project.full_amount == charity_project.invested_amount:
        charity_project.fully_invested = True
        charity_project.close_date = datetime.now()
        session.add(charity_project)
        await session.commit()
        await session.refresh(charity_project)
    return charity_project


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
        charity_project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=CANT_CLOSE_OR_DELETE_ERROR
        )
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=CANT_CLOSE_OR_DELETE_ERROR
        )
    charity_project = await charity_project_crud.remove(
        charity_project, session
    )
    return charity_project
