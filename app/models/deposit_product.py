from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.bank import Bank
    from app.models.deposit_variant import DepositVariant


class DepositProduct(Base):
    __tablename__ = "deposit_products"

    id: Mapped[int] = mapped_column(primary_key=True)
    bank_id: Mapped[int] = mapped_column(ForeignKey("banks.id", ondelete="CASCADE"), index=True)

    name: Mapped[str] = mapped_column(String(250), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="RUB")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    bank: Mapped["Bank"] = relationship(back_populates="deposit_products")
    variants: Mapped[list["DepositVariant"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
    )