from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


PROJECT_EXIST = 'Проект с таким именем уже существует!'
PROJECT_NOT_FOUND = 'Проект не найден!'


async def check_charity_project_name_duplicate(
        charity_project_name: str,
        session: AsyncSession,
) -> None:
    charity_project_id = await (
        charity_project_crud.get_id_by_name(
            charity_project_name,
            session
        )
    )
    if charity_project_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=PROJECT_EXIST
        )


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        charity_project_id, session
    )
    if not charity_project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=PROJECT_NOT_FOUND
        )
    return charity_project


async def check_charity_project_exists_for_update(
        charity_project: CharityProject,
        charity_project_id: int,
        session: AsyncSession,
) -> None:
    select_query = select(CharityProject).where(
        CharityProject.name == charity_project.name
    )
    select_query = select_query.where(
        CharityProject.id != charity_project_id
    )
    charity_project = await session.execute(select_query)
    charity_project = charity_project.scalars().all()
    if charity_project:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=PROJECT_EXIST
        )
    return
