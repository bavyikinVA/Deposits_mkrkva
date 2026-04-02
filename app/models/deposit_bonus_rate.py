from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING, Any
from sqlalchemy import (
    Boolean, CheckConstraint, ForeignKey, Index, Numeric,
    String, Text, Date, Enum as SqlEnum)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import BonusTypeEnum, ConditionTypeEnum


if TYPE_CHECKING:
    from app.models.deposit_variant import DepositVariant


class DepositRateBonus(Base):
    __tablename__ = "deposit_rate_bonuses"
    __table_args__ = (
        CheckConstraint("bonus_value >= 0", name="ck_bonus_value_non_negative"),
        Index("ix_bonus_variant_type", "variant_id", "bonus_type"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    variant_id: Mapped[int] = mapped_column(
        ForeignKey("deposit_variants.id", ondelete="CASCADE"),
        index=True,
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    bonus_type: Mapped[BonusTypeEnum] = mapped_column(
        SqlEnum(BonusTypeEnum, name="bonus_type_enum"),
        nullable=False)

    bonus_value: Mapped[float] = mapped_column(Numeric(7, 4), nullable=False)
    is_percent_points: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    stackable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    priority: Mapped[int] = mapped_column(nullable=False, default=100)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    effective_from: Mapped[date] = mapped_column(Date, nullable=False)
    effective_to: Mapped[date | None] = mapped_column(Date, nullable=True)

    variant: Mapped["DepositVariant"] = relationship(back_populates="bonuses")
    conditions: Mapped[list["DepositRateBonusCondition"]] = relationship(
        back_populates="bonus",
        cascade="all, delete-orphan",
    )


class DepositRateBonusCondition(Base):
    __tablename__ = "deposit_rate_bonus_conditions"
    __table_args__ = (
        Index("ix_bonus_conditions_bonus_id", "bonus_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    bonus_id: Mapped[int] = mapped_column(
        ForeignKey("deposit_rate_bonuses.id", ondelete="CASCADE"),
        index=True,
    )
    condition_type: Mapped[ConditionTypeEnum] = mapped_column(
        SqlEnum(ConditionTypeEnum, name="condition_type_enum"),
        nullable=False,
    )
    field_name: Mapped[str] = mapped_column(String(100), nullable=False)
    operator: Mapped[str] = mapped_column(String(20), nullable=False, default="eq")
    value_json: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)

    bonus: Mapped["DepositRateBonus"] = relationship(back_populates="conditions")