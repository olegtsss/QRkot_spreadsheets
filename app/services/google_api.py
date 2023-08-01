import copy
from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings


FORMAT = '%Y/%m/%d %H:%M:%S'
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
        locale='ru_RU'
    ),
    sheets=[dict(properties=dict(
        sheetType='GRID',
        sheetId=0,
        title='Лист1',
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


async def spreadsheets_create(
    wrapper_services: Aiogoogle,
    spreadsheet_body: str = SPREADSHEET_BODY
) -> str:
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body['properties']['title'] = (
        f'Отчет от {datetime.now().strftime(FORMAT)}'
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
    charity_projects = sorted(
        [
            (
                charity_project.name,
                str(charity_project.close_date - charity_project.create_date),
                charity_project.description
            )
            for charity_project in charity_projects
        ], key=lambda charity_project: charity_project[1]
    )
    service = await wrapper_services.discover('sheets', 'v4')
    table_value = copy.deepcopy(TABLE_VALUE)
    table_value[0].append(datetime.now().strftime(FORMAT))
    table_values = [
        *table_value,
        *[
            list(map(str, charity_project))
            for charity_project in charity_projects
        ]
    ]
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    current_len_table = len(table_values)
    if current_len_table > SHEET_GRID_PROPERTY_ROW_COUNT:
        raise ValueError(
            ROW_COUNT_ERROR.format(count=current_len_table)
        )
    current_max_column_table = max(map(len, table_values))
    if current_max_column_table > SHEET_GRID_PROPERTY_COLUMN_COUNT:
        raise ValueError(
            COLUMN_COUNT_ERROR.format(count=current_max_column_table)
        )
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=f'R1C1:R{current_len_table}C{current_max_column_table}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
