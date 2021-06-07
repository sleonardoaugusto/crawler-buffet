from attr import dataclass


@dataclass
class Stock:
    symbol: str
    name: str
    price: float

    def serialize(self):
        return self.__dict__
