from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.deposit_product import DepositProduct
    from app.models.open_method import DepositVariantOpenMethod
    from app.models.deposit_base_rate import DepositBaseRate
    from app.models.deposit_bonus_rate import DepositRateBonus
    from app.models.deposit_constraint import DepositConstraint
    from app.models.deposit_interest_scheme import DepositInterestScheme
    from app.models.deposit_early_termination_rule import DepositEarlyTerminationRule
    from app.models.deposit_fee import DepositFee


class DepositVariant(Base):
    __tablename__ = "deposit_variants"
    __table_args__ = (
        CheckConstraint("min_amount >= 0", name="ck_variant_min_amount_non_negative"),
        CheckConstraint(
            "max_amount IS NULL OR max_amount >= min_amount",
            name="ck_variant_max_amount_gte_min_amount",
        ),
        CheckConstraint("min_term_days > 0", name="ck_variant_min_term_positive"),
        CheckConstraint(
            "max_term_days IS NULL OR max_term_days >= min_term_days",
            name="ck_variant_max_term_gte_min_term",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    product_id: Mapped[int] = mapped_column(
        ForeignKey("deposit_products.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    allow_topup: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    allow_partial_withdraw: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    auto_prolongation: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    min_amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    max_amount: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)

    min_term_days: Mapped[int] = mapped_column(nullable=False)
    max_term_days: Mapped[int | None] = mapped_column(nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    product: Mapped["DepositProduct"] = relationship(back_populates="variants")

    open_methods: Mapped[list["DepositVariantOpenMethod"]] = relationship(
        back_populates="variant",
        cascade="all, delete-orphan",
    )

    interest_schemes: Mapped[list["DepositInterestScheme"]] = relationship(
        back_populates="variant",
        cascade="all, delete-orphan",
    )

    base_rates: Mapped[list["DepositBaseRate"]] = relationship(
        back_populates="variant",
        cascade="all, delete-orphan",
    )

    bonuses: Mapped[list["DepositRateBonus"]] = relationship(
        back_populates="variant",
        cascade="all, delete-orphan",
    )

    constraints: Mapped[list["DepositConstraint"]] = relationship(
        back_populates="variant",
        cascade="all, delete-orphan",
    )

    early_termination_rules: Mapped[list["DepositEarlyTerminationRule"]] = relationship(
        back_populates="variant",
        cascade="all, delete-orphan",
    )

    fees: Mapped[list["DepositFee"]] = relationship(
        back_populates="variant",
        cascade="all, delete-orphan",
    )