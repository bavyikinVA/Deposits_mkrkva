from enum import Enum

class CurrencyEnum(str, Enum):
    RUB = 'RUB'
    USD = 'USD'
    EUR = 'EUR'
    CNY = 'CNY'

class InterestPayoutTypeEnum(str, Enum):
    END = 'end'
    MONTHLY = 'monthly'

class BonusTypeEnum(str, Enum):
    SUBSCRIPTION = 'subscription'
    SALARY = 'salary'
    PENSION = 'pension'
    SPEND = 'spend'
    SAVINGS_BALANCE = "savings_balance"
    PREMIUM_PACKAGE = 'premium_package'
    PROMO = 'promo'
    OTHER = 'other'

class ConditionTypeEnum(str, Enum):
    BOOLEAN = 'boolean'
    MIN_VALUE = 'min_value'
    ENUM = 'enum'
    JSON_RULE = 'json_rule'

class ConstraintTypeEnum(str, Enum):
    TOPUP_RULE = 'topup_rule'
    AMOUNT_CAP_RULE = 'amount_cap_rule'
    EARLY_TERMINATION_RULE = 'early_termination_rule'
    PROLONGATION_RULE = 'prolongation_rule'
    WITHDRAW_RULE = 'withdraw_rule'
    OTHER = 'other'