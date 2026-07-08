from pyrogram import raw
from ..object import Object


class RefundedPayment(Object):
    def __init__(self, *, currency: str, total_amount: str, invoice_payload: str, telegram_payment_charge_id: str, provider_payment_charge_id: str):
        super().__init__()
        self.currency = currency
        self.total_amount = total_amount
        self.invoice_payload = invoice_payload
        self.telegram_payment_charge_id = telegram_payment_charge_id
        self.provider_payment_charge_id = provider_payment_charge_id

    @staticmethod
    def _parse(client, refunded_payment: "raw.types.MessageActionPaymentRefunded"):
        try:
            invoice_payload = refunded_payment.payload.decode()
        except (UnicodeDecodeError, AttributeError):
            invoice_payload = getattr(refunded_payment, 'payload', None)
        return RefundedPayment(
            currency=refunded_payment.currency,
            total_amount=refunded_payment.total_amount,
            invoice_payload=invoice_payload,
            telegram_payment_charge_id=refunded_payment.charge.id,
            provider_payment_charge_id=refunded_payment.charge.provider_charge_id,
        )
