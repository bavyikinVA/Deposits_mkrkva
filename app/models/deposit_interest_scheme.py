from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.deposit_variant import DepositVariant
    from app.models.deposit_base_rate import DepositBaseRate


class DepositInterestScheme(Base):
    __tablename__ = "deposit_interest_schemes"
    __table_args__ = (
        UniqueConstraint("variant_id", "code", name="uq_interest_scheme_variant_code"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    variant_id: Mapped[int] = mapped_column(
        ForeignKey("deposit_variants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    code: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    payout_type: Mapped[str] = mapped_column(String(50), nullable=False)
    payout_frequency: Mapped[str | None] = mapped_column(String(50), nullable=True)

    capitalization_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    capitalization_frequency: Mapped[str | None] = mapped_column(String(50), nullable=True)

    interest_to_separate_account: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    interest_to_deposit_body: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    nominal_rate_only: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    effective_rate_supported: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    variant: Mapped["DepositVariant"] = relationship(back_populates="interest_schemes")

    base_rates: Mapped[list["DepositBaseRate"]] = relationship(
        back_populates="interest_scheme",
        cascade="all, delete-orphan",
    )