from dataclasses import dataclass


@dataclass

class Prodotto:
    product_id: int
    product_name: str
    brand_id: int
    category_id: int
    model_year: int
    list_price: float
    num_vendite: int = 0
    peso_archi_uscenti: int = 0
    peso_archi_entranti: int = 0

    def __hash__(self):
        return hash(self.product_id)

    def __eq__(self, other):
        return self.product_id == other.product_id

    def __str__(self):
        return f"{self.product_name} - ({self.category_id})"