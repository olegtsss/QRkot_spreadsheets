from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.config import settings
from app.models.project_base import ProjectBase


REPRESENTATION = 'Donation: {base}, user_id={user_id}, comment={comment}'


class Donation(ProjectBase):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self):
        return REPRESENTATION.format(
            base=super().__repr__(),
            user_id=self.user_id,
            comment=self.comment[:settings.attribute_length_slice]
        )
