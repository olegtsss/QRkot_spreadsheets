from http import HTTPStatus
from typing import Dict

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.services.google_api import (
    GoogleException, set_user_permissions, spreadsheets_create,
    spreadsheets_update_value
)


ERROR = 'Ошибка: {error}'
SPREAD_SHEET_URL = 'https://docs.google.com/spreadsheets/d/{spreadsheet_id}'


router = APIRouter()


@router.post(
    '/',
    response_model=Dict,
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
    spreadsheet_id = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheet_id, wrapper_services)
    try:
        await spreadsheets_update_value(
            spreadsheet_id, charity_projects, wrapper_services
        )
    except GoogleException as error:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ERROR.format(error=error)
        )
    return {
        'url': SPREAD_SHEET_URL.format(spreadsheet_id=spreadsheet_id)
    }
