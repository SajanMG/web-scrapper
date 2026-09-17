from dataclasses import dataclass, asdict

@dataclass
class Product:
    name: str
    current_price: float
    currency: str
    product_url: str
    source: str

    regular_price: float | None = None
    unit_price: float | None = None
    unit: str | None = None
    on_special: bool = False
    available: bool = True

    def to_dict(self):
        return asdict(self)