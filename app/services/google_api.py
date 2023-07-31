from datetime import datetime
from http import HTTPStatus

from aiogoogle import Aiogoogle
from fastapi import HTTPException

from app.core.config import settings


FORMAT = '%Y/%m/%d %H:%M:%S'
PROPERTY_TITLE = 'Отчет от {now_datetime}'
PROPERTY_LOCALE = 'ru_RU'
SHEET_TYPE = 'GRID'
SHEET_ID = 0
SHEET_TITLE = 'Лист1'
SHEET_GRID_PROPERTY_ROW_COUNT = 100
SHEET_GRID_PROPERTY_COLUMN_COUNT = 11
ROW_COUNT_ERROR = (
    f'Количество строк в созданной таблице {SHEET_GRID_PROPERTY_ROW_COUNT},'
    'получено строк {count}!'
)
COLUMN_COUNT_ERROR = (
    'Количество столбцов в созданной таблице '
    f'{SHEET_GRID_PROPERTY_COLUMN_COUNT},'
    'получено столбцов {count}!'
)
SPREADSHEET_BODY = dict(
    properties=dict(
        title=PROPERTY_TITLE,
        locale=PROPERTY_LOCALE
    ),
    sheets=[dict(properties=dict(
        sheetType=SHEET_TYPE,
        sheetId=SHEET_ID,
        title=SHEET_TITLE,
        gridProperties=dict(
            rowCount=SHEET_GRID_PROPERTY_ROW_COUNT,
            columnCount=SHEET_GRID_PROPERTY_COLUMN_COUNT
        )
    ))]
)
TABLE_VALUE = [
    ['Отчет от'],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]


class GoogleException(Exception):
    pass


async def spreadsheets_create(
    wrapper_services: Aiogoogle,
    spreadsheet_body: str = SPREADSHEET_BODY
) -> str:
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body['properties']['title'].format(
        now_datetime=datetime.now().strftime(FORMAT)
    )
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email
    }
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields="id"
        )
    )


async def spreadsheets_update_value(
        spreadsheetid: str,
        charity_projects: list,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        *TABLE_VALUE,
        *[
            list(map(str, charity_project))
            for charity_project in charity_projects
        ]
    ]
    table_values[0].append(datetime.now().strftime(FORMAT))
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    current_len_table = len(table_values)
    if current_len_table > SHEET_GRID_PROPERTY_ROW_COUNT:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ROW_COUNT_ERROR.format(count=current_len_table)
        )
    current_max_column_table = max(map(len, table_values))
    if current_max_column_table > SHEET_GRID_PROPERTY_COLUMN_COUNT:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=COLUMN_COUNT_ERROR.format(count=current_max_column_table)
        )
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=f'R1C1:R{current_len_table}C{current_max_column_table}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
