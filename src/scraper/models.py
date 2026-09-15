from dataclasses import dataclass, asdict


@dataclass
class Product:
    name: str
    price: float
    currency: str
    product_url: str
    source: str

    def to_dict(self):
        return asdict(self)