from app.crud.inventory import inventory_crud


class InventoryRepository:
    def __init__(self):
        self.crud = inventory_crud


inventory_repository = InventoryRepository()