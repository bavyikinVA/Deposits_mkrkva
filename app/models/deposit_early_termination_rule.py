from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, Any

from sqlalchemy import ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.deposit_variant import DepositVariant


class DepositEarlyTerminationRule(Base):
    __tablename__ = "deposit_early_termination_rules"

    id: Mapped[int] = mapped_column(primary_key=True)

    variant_id: Mapped[int] = mapped_column(
        ForeignKey("deposit_variants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    rule_type: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    nominal_rate: Mapped[Decimal | None] = mapped_column(Numeric(7, 4), nullable=True)
    effective_rate: Mapped[Decimal | None] = mapped_column(Numeric(7, 4), nullable=True)

    params_json: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)

    variant: Mapped["DepositVariant"] = relationship(back_populates="early_termination_rules")