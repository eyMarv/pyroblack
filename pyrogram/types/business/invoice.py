from typing import Optional, Union

from pyrogram import raw, types
from ..object import Object


class Invoice(Object):
    def __init__(self, *, client=None, currency: str, is_test: bool, title: Optional[str] = None, description: Optional[str] = None, total_amount: Optional[int] = None, start_parameter: Optional[str] = None, prices: Optional[list["types.LabeledPrice"]] = None, is_name_requested: Optional[bool] = None, is_phone_requested: Optional[bool] = None, is_email_requested: Optional[bool] = None, is_shipping_address_requested: Optional[bool] = None, is_flexible: Optional[bool] = None, is_phone_to_provider: Optional[bool] = None, is_email_to_provider: Optional[bool] = None, is_recurring: Optional[bool] = None, max_tip_amount: Optional[int] = None, suggested_tip_amounts: Optional[list[int]] = None, terms_url: Optional[str] = None, _raw: Union["raw.types.MessageMediaInvoice", "raw.types.Invoice"] = None):
        super().__init__(client)
        self.currency = currency
        self.is_test = is_test
        self.title = title
        self.description = description
        self.total_amount = total_amount
        self.start_parameter = start_parameter
        self.prices = prices
        self.is_name_requested = is_name_requested
        self.is_phone_requested = is_phone_requested
        self.is_email_requested = is_email_requested
        self.is_shipping_address_requested = is_shipping_address_requested
        self.is_flexible = is_flexible
        self.is_phone_to_provider = is_phone_to_provider
        self.is_email_to_provider = is_email_to_provider
        self.is_recurring = is_recurring
        self.max_tip_amount = max_tip_amount
        self.suggested_tip_amounts = suggested_tip_amounts
        self.terms_url = terms_url
        self._raw = _raw

    @staticmethod
    def _parse(client, invoice):
        return Invoice(
            currency=invoice.currency,
            is_test=invoice.test,
            title=getattr(invoice, "title", None),
            description=getattr(invoice, "description", None),
            total_amount=getattr(invoice, "total_amount", None),
            start_parameter=getattr(invoice, "start_param", None) or None,
            prices=types.List(types.LabeledPrice._parse(lp) for lp in invoice.prices) if getattr(invoice, "prices", None) else None,
            is_name_requested=getattr(invoice, "name_requested", None),
            is_phone_requested=getattr(invoice, "phone_requested", None),
            is_email_requested=getattr(invoice, "email_requested", None),
            is_shipping_address_requested=getattr(invoice, "shipping_address_requested", None),
            is_flexible=getattr(invoice, "flexible", None),
            is_phone_to_provider=getattr(invoice, "phone_to_provider", None),
            is_email_to_provider=getattr(invoice, "email_to_provider", None),
            is_recurring=getattr(invoice, "recurring", None),
            max_tip_amount=getattr(invoice, "max_tip_amount", None),
            suggested_tip_amounts=getattr(invoice, "suggested_tip_amounts", None) or None,
            terms_url=getattr(invoice, "terms_url", None),
            _raw=invoice,
            client=client,
        )
