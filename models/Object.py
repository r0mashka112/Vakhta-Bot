from .Base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Object(Base):
    __tablename__ = 'objects'

    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(unique = True)

    attendances = relationship("Attendance", back_populates = "objects")