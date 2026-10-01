from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL")
    )
    is_active: Mapped[bool] = mapped_column(default=True)

    parent: Mapped["Category | None"] = relationship(
        back_populates="children",
        remote_side="Category.id"
    )
    children: Mapped[list["Category"]] = relationship(back_populates="parent")
    products: Mapped[list["Product"]] = relationship(back_populates="category")
