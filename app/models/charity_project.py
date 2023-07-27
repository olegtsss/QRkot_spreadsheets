from sqlalchemy import Column, String, Text

from app.core.config import settings
from app.models.project_base import ProjectBase


REPRESENTATION = (
    'CharityProject: {base}, name={name}, description={description}'
)


class CharityProject(ProjectBase):
    name = Column(
        String(settings.charity_project_name_max), unique=True, nullable=False
    )
    description = Column(Text, nullable=False)

    def __repr__(self):
        return REPRESENTATION.format(
            base=super().__repr__(),
            name=self.name[:settings.attribute_length_slice],
            description=self.description[:settings.attribute_length_slice]
        )
