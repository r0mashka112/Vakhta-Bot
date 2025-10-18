from .Base import Base
from datetime import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import (
    User,
    Object
)

class Attendance(Base):
    __tablename__ = 'attendances'

    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    object_id: Mapped[int] = mapped_column(ForeignKey('objects.id'))
    date: Mapped[str]
    action: Mapped[str]
    note: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(server_default = func.now())

    user: Mapped['User'] = relationship(
        'User',
        back_populates = 'attendances'
    )

    object: Mapped['Object'] = relationship(
        'Object',
        back_populates = 'attendances'
    )