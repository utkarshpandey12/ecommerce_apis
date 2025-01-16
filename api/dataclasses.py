from dataclasses import dataclass

from api.exceptions import InvaidSchemaException


@dataclass
class ProductData:
    id: int
    quantity: int

    @staticmethod
    def from_json(data):
        try:
            return ProductData(id=data["id"], quantity=data["quantity"])
        except Exception:
            raise InvaidSchemaException

    def to_json(self):
        return {"id": self.id, "quantity": self.quantity}
