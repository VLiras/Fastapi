from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

route = APIRouter(prefix='/users', tags=['Users'])

# Defino una identidad atraves de una "class"
class User (BaseModel): 
    # Con BaseModel, puedo crear una entidad y me lo convierte automaticamente en un objeto JSON
    id: int 
    name: str 
    lastName:str 
    age: int
    email: str

users_list = [
    User(id = 1,name='Pablo', lastName='Gutierrez', age = 20, email='pablo@gmail.com'),
    User(id = 2,name='Martin', lastName='Rodriguez', age = 23, email='martin@gmail.com'),
    User(id = 3, name='Benjamin', lastName='Liras',  age = 18, email='benja@gmail.com')
]

@route.get('/')
async def users():
    # Doy un ejemplo enviando un JSON manualmente
    # return [
        # {'id':'1','name':'Pablo','lastName':'Gutierrez','age':'20'},
        # {'id':'2','name':'Benjamin','lastName':'Liras','age':'18'}    
    #]
    return users_list

# Path
@route.get('/{id}')
async def getUser(id: int):
    return search(id)
    
# Query
@route.get('/user/')
async def getQuery(id: int):
    return search(id)

def search (id: int):
    user = filter(lambda user: user.id, users_list) 
    # filter => Funcion de orden superior => Nativa de Python
    try:
        return list(user)[id - 1]
    except:
        return f'Usuario no encontrado: ¿¿{id}??'
    
@route.post('/user/', response_model = User, status_code = 201)
# Le paso un usuario como argumento para poder agregar un usuario
async def postUser(user: User):
    if type(search(user.id)) == User:
        raise HTTPException(status_code = 400, detail='Este usuario ya existe')
        # print(type(search(user.id)))
    else:
        users_list.append(user)
        # return 'El usuario se ha añadido correctamente'
        # return user
        return users_list

@route.put('/user/')
async def update_user(user: User):
    # Le paso de argumento el objeto a actualizar
    found = False
    for index, saved in enumerate(users_list):
        if saved.id == user.id:
            users_list[index] == user
            found = True
        # return users_list
    if not found:
        return 'No se puede actualizar un usuario inexistente', found
    else: 
        return user, found, users_list


@route.delete('/user/{id}')
async def delete_user(id: int):
    found = False
    for index, saved in enumerate(users_list):
        if saved.id == id:
            del users_list[index]
            found = True
            return users_list, found
    if not found:
        return 'El usuario no se ha eliminado', found, users_list
        