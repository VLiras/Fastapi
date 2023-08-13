from fastapi import APIRouter
route = APIRouter(prefix='/products', 
                  tags=['products'], 
                  responses={404:{'message':'Not Found'}})

products_list = ['Producto 1', 'Producto 2', 'Producto 3']
@route.get('/')
async def products():
    return products_list


@route.get('/{id}')
async def products(id: int):
    return products_list[id]