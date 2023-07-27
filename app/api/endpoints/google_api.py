from typing import List

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.services.google_api import (
    set_user_permissions, spreadsheets_create, spreadsheets_update_value,
    take_charity_projects_by_shorts
)


router = APIRouter()


@router.post(
    '/',
    response_model=List,
    dependencies=[Depends(current_superuser)],
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)
):
    """Только для суперюзеров."""
    charity_projects = (
        await charity_project_crud.get_projects_by_completion_rate(session)
    )
    results = [
        (
            charity_project.name,
            str(charity_project.close_date - charity_project.create_date),
            charity_project.description
        ) for charity_project in charity_projects
    ]
    results = sorted(results, key=take_charity_projects_by_shorts)
    spreadsheetid = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheetid, wrapper_services)
    await spreadsheets_update_value(spreadsheetid, results, wrapper_services)
    return results
