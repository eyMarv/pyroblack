from datetime import datetime
from pyrogram import raw, types, utils
from ..object import Object


class SuccessfulPayment(Object):
    def __init__(self, *, currency: str, total_amount: str, invoice_payload: str, subscription_expiration_date: datetime = None, is_recurring: bool = None, is_first_recurring: bool = None, shipping_option_id: str = None, order_info: "types.OrderInfo" = None, telegram_payment_charge_id: str, provider_payment_charge_id: str, invoice_name: str = None):
        super().__init__()
        self.currency = currency
        self.total_amount = total_amount
        self.invoice_payload = invoice_payload
        self.subscription_expiration_date = subscription_expiration_date
        self.is_recurring = is_recurring
        self.is_first_recurring = is_first_recurring
        self.shipping_option_id = shipping_option_id
        self.order_info = order_info
        self.telegram_payment_charge_id = telegram_payment_charge_id
        self.provider_payment_charge_id = provider_payment_charge_id
        self.invoice_name = invoice_name

    @staticmethod
    def _parse(client, successful_payment):
        invoice_payload = None
        telegram_payment_charge_id = None
        provider_payment_charge_id = None
        shipping_option_id = None
        order_info = None
        if isinstance(successful_payment, raw.types.MessageActionPaymentSentMe):
            try:
                invoice_payload = successful_payment.payload.decode()
            except (UnicodeDecodeError, AttributeError):
                invoice_payload = successful_payment.payload
            telegram_payment_charge_id = successful_payment.charge.id
            provider_payment_charge_id = successful_payment.charge.provider_charge_id
            shipping_option_id = getattr(successful_payment, 'shipping_option_id', None)
            if successful_payment.info:
                payment_info = successful_payment.info
                order_info = types.OrderInfo(
                    name=getattr(payment_info, 'name', None),
                    phone_number=getattr(payment_info, 'phone', None),
                    email=getattr(payment_info, 'email', None),
                    shipping_address=types.ShippingAddress(
                        country_code=payment_info.shipping_address.country_iso2,
                        state=payment_info.shipping_address.state,
                        city=payment_info.shipping_address.city,
                        street_line1=payment_info.shipping_address.street_line1,
                        street_line2=payment_info.shipping_address.street_line2,
                        post_code=payment_info.shipping_address.post_code,
                    )
                )
        return SuccessfulPayment(
            currency=successful_payment.currency,
            total_amount=successful_payment.total_amount,
            invoice_payload=invoice_payload,
            telegram_payment_charge_id=telegram_payment_charge_id,
            provider_payment_charge_id=provider_payment_charge_id,
            shipping_option_id=shipping_option_id,
            order_info=order_info,
            is_recurring=getattr(successful_payment, 'recurring_used', None),
            is_first_recurring=getattr(successful_payment, 'recurring_init', None),
            invoice_name=getattr(successful_payment, 'invoice_slug', None),
            subscription_expiration_date=utils.timestamp_to_datetime(successful_payment.subscription_until_date),
        )
