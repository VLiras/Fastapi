from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "00290a96067dcfcbd1678529ae5609efdb45c5d04ec8dbd1210051f21006179b"
route = APIRouter()
# JWT => JSON Web Token 

oauth2 = OAuth2PasswordBearer(tokenUrl="login")
# Creo un contexto de encriptacion
crypt = CryptContext(schemes=["bcrypt"])
# Los "schemes" definen el algoritmo de encriptacion que se va a utilizar
# 5:21.30
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
        "password":"$2a$12$5s9/Kfi33X6Tp6HrLT/egO3iju6o7nTquPh4Uu4W0EpOcs49WUhCq"
    },
    "pablux":{
        "username": "pablux",
        "name": "Pablo",
        "email": "pablux@gmail.com",
        "disabled": True,
        "password":"$2a$12$YBKmvW99IIpD/GO4q9vN5OG2DYUsfqRTwt/wXSkj6MVWLOAn9F1oK"
    },
}
def searchUserDb(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def searchUser(username: str):
    if username in users_db:
        return User(**users_db[username])
    
@route.post('/login')
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario incorrecto")
    
    user = searchUserDb(form.username)

    # crypt.verify => Compara la contraseña original (la ingresada) con la encritada
    # Aparte de encriptar la contraseña, debemos hacer los mismo con el token de autenticacion proporcionado

    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contraseña incorrecta")

    # El access_token va a ser de tipo JWT, donde uno de los parametros  es cuanto tiempo durara dicho token

    # Para añadirle seguridad, le podemos añadir una semilla generada que solo conzca el backend para la encriptacion y deencriptacion. 
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    access_token = {"sub":user.username,"exp":expire}
    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type":"bearer"}

def searchUser(username: str):
    if username in users_db:
        return User(**users_db[username])

async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales de autenticacion invalidas", 
            headers={"WWW-Authenticated": "bearer"})
    try:
        userName = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if userName is None: 
            raise exception
    except JWTError:
         raise exception
    return searchUser(userName)
       

async def currentUser(user: User = Depends(auth_user)):
    if user.disabled: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Usuario inactivo")
    return user

@route.get("/users/me")
async def me(user: User = Depends(currentUser)):
    return user