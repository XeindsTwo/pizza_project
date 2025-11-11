from pydantic import BaseModel
from typing import Optional

class Pizza(BaseModel):
    id: Optional[int] = None # присвоим ID при добавлении, чтобы не возникало ошибок
    # поле идентификатора будет необязательным в теле запроса (например при добавлении)
    name: str
    price: float
    category_id: Optional[int] = None

