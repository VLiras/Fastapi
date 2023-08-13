## Creando un Backend con FastAPI


#### Path y Query

Path y Query son dos maneras distintas de crear enrutados dinamicos a partir de los datos obtenidos que manejemos (usuarios, autos, casas, productos, etc.)

 - Path:
    Se suele utilizar el path cambio se trata de un parametro obligatorio para datos dinamicos que sean fijos. 

- Query:
    Se pueden utilizar para datos que, en si, no son necesarios para realizar la solicitud, o para pedir datos muy concretos. Sirve para renderizar parte de los datos para no sobrecargar el servidor. 

#### POST, PUT & DELETE
- POST: Lo uso para crear/enviar datos al server. Por ejemplo: al ingresar un usuario y contraseña 
- PUT: Lo utilizo para actualizar datos ya existentes (esten vacios previamente o no). Por ejemplo: cambiar mi contraseña
- DELETE: Para borrar datos. 

#### HTTP codigo de status

- 100 - 199: Informacion (estos son raros de usar directamente)
- 200 - 299:  Solicitud completada de manera exitosa
    - 200: El mas usado, todo esta OK!
    - 201 "Created!": Normalmente, se aplica al añadir nuevos datos a la base.
    - 204 "No Content!": Se aplica cuando no hay contenido que retornarle al usuario, o sea, la respuesta no tiene body. 
- 300 - 399: Redirecciones. 
    Este tipo de solicitudes, dependiendo el caso, pueden portar o no un body en la response. Ej: un 304 ("Not Modify") no deberia porta un body.
- 400 - 499: Errores del Cliente
    - 404 "Not Found": El mas usado, no se encuentra la informacion solicitada. 
    Normalmente, se suele usar el 400 de manera generica para todos los errores de este tipo. 
- 500 - 599: Errores del Servidor, es raro que se los utilice directamente. 
Siempre que lance algun error en Python, usando el meotodo ```HTTPException()```, coloco previamente el metodo ```raise```.
raise: es un metodo que propaga la excepcion, equivalente al ```throw``` en Javascript. 

#### Routers
Para crear rutas dentro de FastAPI dentro de una misma app, importo y utilizo en el archivo de ruta ```APIRouter``` en lugar de FastAPI. Con esto, le indico a FastAPI que esto representa una ruta de la app original.
Luego, en el archivo original agrego lo siguiente ```app.include_router(file.route)```, por supuesto, importando los archivos previamente. 
Ademas, dentro de APIRouter, puedo colocar un "prefix" (prefijo) generico para mis rutas.
Por ejemplo:
```APIRouter(prefix="/algo")```

