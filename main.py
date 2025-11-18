from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse

from models.category_manager import CategoryManager
from models.pizza import Pizza
from models.category import Category
from models.pizza_manager import PizzaManager

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

pizza_manager = PizzaManager()
category_manager = CategoryManager()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def get_pizzas(request: Request):
    categories = category_manager.get_all()
    pizzas = pizza_manager.get_all_with_category(categories)
    return templates.TemplateResponse("index.html", {"request": request, "pizzas": pizzas})


@app.get("/pizzas/add")
def add_pizza_form(request: Request):
    categories = category_manager.get_all()
    return templates.TemplateResponse("add_pizza.html", {"request": request, "categories": categories})


@app.post("/pizzas/add")
def add_pizza(
    name: str = Form(...),
    price: float = Form(...),
    category_id: int = Form(...),
):
    # чтобы FastAPI умел принимать данные из формы через Form(...), нужен пакет python-multipart
    categories = category_manager.get_all()
    pizza = Pizza(name=name, price=price, category_id=category_id)
    pizza_manager.add_pizza(pizza, categories)
    return RedirectResponse(url="/", status_code=303)


@app.put("/pizzas/edit")
def edit_pizza(pizza: Pizza):
    categories = category_manager.get_all()
    return pizza_manager.edit_pizza(pizza.id, pizza.name, pizza.price, pizza.category_id, categories)


@app.delete("/pizzas/delete/{pizza_id}")
def delete_pizza(pizza_id: int):
    return pizza_manager.delete_pizza(pizza_id)


@app.get("/categories")
def get_categories():
    return category_manager.get_all()


@app.post("/categories/add")
def add_category(category: Category):
    return category_manager.add_category(category)


@app.put("/categories/edit")
def edit_category(category: Category):
    return category_manager.edit_category(category.id, category.name)


@app.delete("/categories/delete/{category_id}")
def delete_category(category_id: int):
    return category_manager.delete_category(category_id)
