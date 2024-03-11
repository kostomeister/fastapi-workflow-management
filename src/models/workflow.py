from sqlalchemy.orm import Mapped, mapped_column

from src.db.db import Base


class Workflow(Base):
    __tablename__ = "workflows"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    file_url: Mapped[str]
