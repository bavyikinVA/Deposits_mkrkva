from __future__ import annotations

from typing import TYPE_CHECKING, Any

from sqlalchemy import ForeignKey, Index, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import ConstraintTypeEnum

if TYPE_CHECKING:
    from app.models.deposit_variant import DepositVariant


class DepositConstraint(Base):
    __tablename__ = "deposit_constraints"
    __table_args__ = (
        Index("ix_constraints_variant_type", "variant_id", "constraint_type"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    variant_id: Mapped[int] = mapped_column(
        ForeignKey("deposit_variants.id", ondelete="CASCADE"),
        index=True,
    )

    constraint_type: Mapped[ConstraintTypeEnum] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    params_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)

    variant: Mapped["DepositVariant"] = relationship(back_populates="constraints")