import json
import os.path

from unicodedata import category

from models.pizza import Pizza


class PizzaManager:
    def __init__(self, path="data/pizzas.json"):
        self.path = path
        self.pizzas = []
        self._load()

    def _load(self):
        if os.path.isfile(self.path):
            with open(self.path, 'r', encoding='utf-8') as file:
                try:
                    self.pizzas = [Pizza(**item) for item in json.load(file)]
                except json.JSONDecodeError:
                    self.pizzas = []
        else:
            with open(self.path, 'w', encoding='utf-8') as file:
                json.dump([], file, ensure_ascii=False, indent=4)
            self.pizzas = []

    def _save(self):
        with open(self.path, 'w', encoding='utf-8') as file:
            json.dump([pizza.dict() for pizza in self.pizzas], file, ensure_ascii=False, indent=4)

    def get_all(self):
        return self.pizzas

    def get_all_with_category(self, categories):
        result = []
        for pizza in self.pizzas:
            category_name = next((cat.name for cat in categories if cat.id == pizza.category_id), None)
            result.append({
                "id": pizza.id,
                "name": pizza.name,
                "price": pizza.price,
                "category_id": pizza.category_id,
                "category_name": category_name
            })
        return result

    def add_pizza(self, pizza: Pizza, categories) -> dict:
        if pizza.category_id is not None:
            category_exists = any(cat.id == pizza.category_id for cat in categories)
            if not category_exists:
                return {"message": "Категории с таким идентификатором не существует"}

        if self.pizzas:
            new_id = self.pizzas[-1].id + 1
        else:
            new_id = 1
        pizza.id = new_id
        self.pizzas.append(pizza)
        self._save()
        return {
            "message": "Пицца успешно добавлена",
            "pizza": pizza
        }

    def edit_pizza(self, pizza_id: int, new_name: str, new_price: float, category_id: int, categories) -> dict:
        pizza_to_edit = next((pizza for pizza in self.pizzas if pizza.id == pizza_id), None)
        if not pizza_to_edit:
            return {"message": "Пицца с таким ID не найдена"}

        if category_id is not None:
            category_exists = any(cat.id == category_id for cat in categories)
            if not category_exists:
                return {"message": "Категории с таким идентификатором не существует"}

        pizza_to_edit.name = new_name
        pizza_to_edit.price = new_price
        pizza_to_edit.category_id = category_id
        self._save()
        return {
            "message": f"Пицца с идентификатором {pizza_to_edit.id} успешно обновлена",
            "pizza": pizza_to_edit
        }

    def delete_pizza(self, pizza_id: int) -> dict:
        pizza_to_delete = next((pizza for pizza in self.pizzas if pizza.id == pizza_id), None)
        if not pizza_to_delete:
            return {"message": "Пицца с таким ID не найдена"}

        self.pizzas.remove(pizza_to_delete)
        self._save()
        return {"message": f"Пицца с идентификатором {pizza_to_delete.id} успешно удалена"}
