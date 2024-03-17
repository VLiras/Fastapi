from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()
# OAuth2PasswordBearer => Es el que se encarga de gestionar la autenticacion del usuario y contraseña.  
# OAuth2PasswordRequestForm => La forma en la que se envia al backend el criterio de autenticacion y como este captura estos datos para autenticar. 

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "mauri":{
        "username": "mauri",
        "name": "Mauricio",
        "email": "moure@gmail.com",
        "disabled": False,
        "password":"123456"
    },
    "pablux":{
        "username": "pablux",
        "name": "Pablo",
        "email": "pablux@gmail.com",
        "disabled": True,
        "password":"654321"
    },
}
def searchUserDb(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
def searchUser(username: str):
    if username in users_db:
        return User(**users_db[username])

async def currentUser(token: str = Depends(oauth2)):
    user = searchUser(token) # el token es el propio usuario de base de datos

    if not user: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales de autenticacion invalidas", 
            headers={"WWW-Authenticated": "bearer"})
    if user.disabled: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Usuario inactivo")
    return user

# Depends() => Al colocar este parametro, se establece que esta variable puede recibir datos pero no depende de nadie, basicamente. 
@app.post('/login')
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario incorrecto")
    
    user = searchUserDb(form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contraseña incorrecta")
    return {"access_token": user.username, "token_type":"bearer"}

# Una vez autenticados
@app.get("/users/me")
async def me(user: User = Depends(currentUser)):
    return user