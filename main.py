from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from models.pizza import Pizza
from models.manager import PizzaManager

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

pizza_manager = PizzaManager()
templates = Jinja2Templates(directory="templates")

@app.get('/')
def root():
    return {"message": "Добро пожаловать в мир пицц"}

@app.get("/pizzas")
def get_pizzas(request: Request):
    pizzas = pizza_manager.get_all()
    return templates.TemplateResponse("index.html", {"request": request, "pizzas": pizzas})

@app.post("/pizzas/add")
def add_pizza(pizza: Pizza):
    return pizza_manager.add_pizza(pizza)

@app.put("/pizzas/edit")
def edit_pizza(pizza: Pizza):
    return pizza_manager.edit_pizza(pizza.id, pizza.name, pizza.price)

@app.delete("/pizzas/delete/{pizza_id}")
def delete_pizza(pizza_id: int):
    return pizza_manager.delete_pizza(pizza_id)