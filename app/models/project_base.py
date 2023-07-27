from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.db import Base


REPRESENTATION = (
    'id={id}, create={create_date}, close={close_date} '
    'full_amount={full_amount}, invested_amount={invested_amount}'
)


class ProjectBase(Base):
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

    __abstract__ = True
    __table_args__ = (
        CheckConstraint('invested_amount >= 0'),
        CheckConstraint('invested_amount <= full_amount')
    )

    def __repr__(self):
        return REPRESENTATION.format(
            id=self.id,
            create_date=self.create_date,
            close_date=self.close_date,
            full_amount=self.full_amount,
            invested_amount=self.invested_amount,
        )
