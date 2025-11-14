import json
import os.path
from models.category import Category


class CategoryManager:
    def __init__(self, path="data/categories.json"):
        self.path = path
        self.categories = []
        self._load()

    def _load(self):
        if os.path.isfile(self.path):
            with open(self.path, 'r', encoding='utf-8') as file:
                try:
                    self.categories = [Category(**item) for item in json.load(file)]
                except json.JSONDecodeError:
                    self.categories = []
        else:
            with open(self.path, 'w', encoding='utf-8') as file:
                json.dump([], file, ensure_ascii=False, indent=4)
            self.categories = []

    def _save(self):
        with open(self.path, 'w', encoding='utf-8') as file:
            json.dump([cat.dict() for cat in self.categories], file, ensure_ascii=False, indent=4)

    def get_all(self):
        return self.categories

    def add_category(self, category: Category) -> dict:
        if self.categories:
            new_id = self.categories[-1].id + 1
        else:
            new_id = 1
        category.id = new_id
        self.categories.append(category)
        self._save()
        return {
            "message": "Категория успешно добавлена",
            "category": category
        }

    def edit_category(self, category_id: int, new_name: str) -> dict:
        category_to_edit = next((category for category in self.categories if category.id == category_id), None)
        if not category_to_edit:
            return {"message": "Категория с таким ID не найдена"}

        category_to_edit.id = category_id
        category_to_edit.name = new_name
        self._save()
        return {
            "message": f"Категория с идентификатором {category_to_edit.id} успешно обновлена",
            "category": category_to_edit
        }

    def delete_category(self, category_id: int) -> dict:
        category_to_delete = next((category for category in self.categories if category.id == category_id), None)
        if not category_to_delete:
            return {"message": "Категория с таким ID не найдена"}

        self.categories.remove(category_to_delete)
        self._save()
        # удаление делаем более мягким, не удаляя вслед за собой пиццы, которые привязаны к удалённой категории
        return {"message": "Категория успешно удалена"}