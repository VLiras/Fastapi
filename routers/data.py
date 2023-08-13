from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import fastapi.middleware.cors
app = FastAPI()

def getDocument():
    doc = open('C:\Back Up Valentín\Valentin\Apps\Fastapi\hello.html', 'r')
    # doc = open('C:\Back Up Valentín\Valentin\Apps\Player\index.html', 'r')
    file = doc.read()
    # print(type(file))
    return file



@app.get('/data')
async def root():
    return 'Hello World'

# Prueba >>> 
# class Data(BaseModel):
#     name: str
#     lastName:str

# @app.post('http://localhost:5173/')
# async def getData(data: Data):
#     itemName = data.name
#     itemLastName = data.lastName
#     print('Data recibida')
#     return {'name':itemName, 'lastName':itemLastName}
    

@app.get('/data/doc', response_class=HTMLResponse)
async def document():
    return getDocument()