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
