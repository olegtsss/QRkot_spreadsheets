from datetime import datetime
from typing import List

from app.models import ProjectBase


def worker(
    target: ProjectBase, sources: List[ProjectBase]
) -> List[ProjectBase]:
    update_sources = []
    for source in sources:
        available_amount = min(
            source.full_amount - source.invested_amount,
            target.full_amount - target.invested_amount
        )
        for object in [target, source]:
            object.invested_amount += available_amount
            if object.invested_amount == object.full_amount:
                object.fully_invested = True
                object.close_date = datetime.now()
        update_sources.append(source)
        if target.fully_invested:
            break
    return update_sources
