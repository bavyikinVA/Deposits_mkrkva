from datetime import date
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.schemas.deposit import (
    DepositCalculationRequest,
    DepositCalculationResult,
    DepositSearchParams,
    DepositsPage,
)
from app.services.deposit_calculator import (
    CalculationContext,
    DepositCalculationError,
    calculate_variant_result,
)
from app.services.deposits import get_variant_or_404, search_deposit_variants

router = APIRouter(prefix="/api/deposits", tags=["deposits"])


@router.get("", response_model=DepositsPage)
async def list_deposits(
    amount: Decimal | None = Query(default=None, gt=0),
    term_days: int | None = Query(default=None, gt=0),
    currency: str | None = Query(default=None, min_length=3, max_length=3),
    bank_ids: list[int] | None = Query(default=None),
    open_method_codes: list[str] | None = Query(default=None),
    interest_scheme_code: str | None = Query(default=None),
    payout_type: str | None = Query(default=None),
    capitalization_enabled: bool | None = Query(default=None),
    allow_topup: bool | None = Query(default=None),
    allow_partial_withdraw: bool | None = Query(default=None),
    auto_prolongation: bool | None = Query(default=None),
    as_of: date = Query(default_factory=date.today),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    session: AsyncSession = Depends(get_session),
):
    params = DepositSearchParams(
        amount=amount,
        term_days=term_days,
        currency=currency,
        bank_ids=bank_ids,
        open_method_codes=open_method_codes,
        interest_scheme_code=interest_scheme_code,
        payout_type=payout_type,
        capitalization_enabled=capitalization_enabled,
        allow_topup=allow_topup,
        allow_partial_withdraw=allow_partial_withdraw,
        auto_prolongation=auto_prolongation,
        as_of=as_of,
        page=page,
        page_size=page_size,
    )
    return await search_deposit_variants(session, params)


@router.post("/search", response_model=DepositsPage)
async def search_deposits(
    payload: DepositSearchParams,
    session: AsyncSession = Depends(get_session),
):
    return await search_deposit_variants(session, payload)


@router.post("/calculate", response_model=DepositCalculationResult)
async def calculate_deposit(
    payload: DepositCalculationRequest,
    session: AsyncSession = Depends(get_session),
):
    try:
        variant = await get_variant_or_404(session, payload.variant_id)

        ctx = CalculationContext(
            amount=payload.amount,
            term_days=payload.term_days,
            as_of=payload.as_of,
            open_method_code=payload.open_method_code,
            interest_scheme_code=payload.interest_scheme_code,
            has_subscription=payload.has_subscription,
            is_salary_client=payload.is_salary_client,
            is_pension_client=payload.is_pension_client,
            monthly_spend=payload.monthly_spend,
            savings_balance=payload.savings_balance,
            has_premium_package=payload.has_premium_package,
            promo_code=payload.promo_code,
            extra_context=payload.extra_context,
        )

        return calculate_variant_result(variant, ctx)

    except DepositCalculationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc