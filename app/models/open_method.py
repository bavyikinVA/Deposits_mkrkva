from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.deposit_variant import DepositVariant
    from app.models.deposit_base_rate import DepositBaseRate

class DepositOpenMethod(Base):
    __tablename__ = "deposit_open_methods"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    variants: Mapped[list["DepositVariantOpenMethod"]] = relationship(
        back_populates="open_method",
        cascade="all, delete-orphan",
    )
    base_rates: Mapped[list["DepositBaseRate"]] = relationship(back_populates="open_method", )


class DepositVariantOpenMethod(Base):
    __tablename__ = "deposit_variant_open_methods"
    __table_args__ = (
        UniqueConstraint("variant_id", "open_method_id", name="uq_variant_open_method"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    variant_id: Mapped[int] = mapped_column(
        ForeignKey("deposit_variants.id", ondelete="CASCADE"),
        index=True,
    )
    open_method_id: Mapped[int] = mapped_column(
        ForeignKey("deposit_open_methods.id", ondelete="CASCADE"),
        index=True,
    )

    variant: Mapped["DepositVariant"] = relationship(back_populates="open_methods")
    open_method: Mapped["DepositOpenMethod"] = relationship(back_populates="variants")