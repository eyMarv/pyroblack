from typing import Optional

from pyrogram import raw

from ..object import Object


class PaymentResult(Object):
    """Contains the result of a payment request."""

    def __init__(
        self,
        *,
        success: bool,
        verification_url: Optional[str] = None,
        raw: "raw.base.payments.PaymentResult" = None,
    ):
        super().__init__()

        self.success = success
        self.verification_url = verification_url
        self.raw = raw

    @staticmethod
    def _parse(payment_result: "raw.base.payments.PaymentResult") -> "PaymentResult":
        if isinstance(payment_result, raw.types.payments.PaymentVerificationNeeded):
            return PaymentResult(
                success=False,
                verification_url=payment_result.url,
                raw=payment_result,
            )

        return PaymentResult(
            success=True,
            raw=payment_result,
        )
