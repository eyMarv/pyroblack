from enum import auto

from .auto_name import AutoName


class PaymentFormType(AutoName):
    """Describes type of payment form."""

    REGULAR = auto()
    STARS = auto()
    STAR_SUBSCRIPTION = auto()
