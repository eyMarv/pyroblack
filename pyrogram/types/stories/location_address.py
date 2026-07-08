from ..object import Object


class LocationAddress(Object):
    def __init__(self, country_code: str = None, state: str = None, city: str = None, street: str = None):
        super().__init__()
        self.country_code = country_code
        self.state = state
        self.city = city
        self.street = street
