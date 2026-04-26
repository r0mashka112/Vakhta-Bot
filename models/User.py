from .Base import Base
from datetime import datetime
from sqlalchemy import ForeignKey, func, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import (
    Attendance,
    Speciality
)

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique = True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    middle_name: Mapped[str | None]
    speciality_id: Mapped[int] = mapped_column(ForeignKey('specialities.id'))
    phone: Mapped[str] = mapped_column(unique = True)
    is_admin: Mapped[bool] = mapped_column(default = False)
    created_at: Mapped[datetime] = mapped_column(server_default = func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default = func.now(),
        onupdate = func.now()
    )

    speciality: Mapped['Speciality'] = relationship(
        'Speciality',
        back_populates = 'users',
        lazy = 'joined',
    )

    attendances: Mapped[list['Attendance']] = relationship(
        'Attendance',
        back_populates = 'user',
        cascade = 'all, delete-orphan'
    )