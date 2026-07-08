from ..object import Object


class OrderInfo(Object):
    def __init__(self, *, name: str = None, phone_number: str = None, email: str = None, shipping_address: "types.ShippingAddress" = None):
        super().__init__()
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.shipping_address = shipping_address
