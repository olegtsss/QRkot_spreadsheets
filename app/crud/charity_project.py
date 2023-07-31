from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_id_by_name(
            self,
            charity_project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        charity_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == charity_project_name
            )
        )
        return charity_project_id.scalars().first()

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> List:
        charity_projects = await session.execute(
            select(
                CharityProject
            ).where(
                CharityProject.fully_invested
            )
        )
        return sorted(
            [
                (
                    charity_project.name,
                    str(
                        charity_project.close_date - charity_project.create_date
                    ),
                    charity_project.description
                ) for charity_project in charity_projects.scalars().all()
            ], key=lambda charity_project: charity_project[1]
        )


charity_project_crud = CRUDCharityProject(CharityProject)
