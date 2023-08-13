# Instalar fastapi => pip install fastapi[all]
from fastapi import FastAPI
from routers import products, users
app = FastAPI()

# Arrancar el servidor => uvicorn main:app --reload
# URL : http://127.0.0.1:8000
class User ():
    def __init__(self, name, lastName, age, id):
        self.id = id
        self.name: str = name
        self.lastName: str = lastName
        self.age: int = age

mi_user = User('Valentin', 'Liras', 20, 1)

# Routers
app.include_router(products.route)
app.include_router(users.route)

@app.get('/')
async def root():
    # return 'Hello World from main'
    return mi_user





