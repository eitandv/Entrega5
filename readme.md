# Entrega 3
Grupos:
- Grupo 41
- Grupo 42

Integrantes:
- Eitan Dvorquez
- Benjamín Lobos
- Andrés Pincheira
- Moisés Retamal


## Para hacer correr la aplicación, abrir la carpeta donde están los archivos("entrega4/") y escribir:
- pipenv install
- pipenv shell
- gunicorn main:app --workers=3 --reload

Una vez ahí proceder a cargar la base de datos.


## Para cargar la base de datos:
ingresar a la carpeta messages.json y ejecutar el comando mongo start(o mongo segun sea el caso)
luego ingresar los siguientes comandos:

- mongoimport --db test --collection users --drop --file users.json --jsonArray
- mongoimport --db test --collection messages --drop --file messages.json --jsonArray


##Consultas:

#Para probar las consultas get

**Mensajes a partir del id**

Entrar en la ruta localhost:(port)/messages/mid donde mid es el id del mensaje y port es el puerto del localhost. Esta función se encuentra implementada con el nombre de get_message en el archivo main.py, y recibe como parametros el id del mensaje a buscar, y retorna un diccionario con la información del mensaje buscado.

**Usuario y mensajes a partir de su id**
Entrar en la ruta localhost:(port)/users/id donde id es el id del usuario a buscar y port es el puerto del localhost. Esta función se encuentra implementada con el nombre de get_user en el archivo main.py, y recibe como parametros el id del usuario que desea ver sus mensajes, y retorna un diccionario con la información del usuario y el contenido de todos sus mensajes enviados.

**Usuarios y mensajes entre ellos**
Entrar en la ruta localhost:(port)/twousers/id1/id2 donde id1 e id2 son los id de los usuarios y port es el puerto del localhost. Esta función se encuentra implementada con el nombre de get_two_users en el archivo main.py, y recibe como parametros el id de los 2 usuarios entre los que se quieren ver los mensajes intercambiados, y retorna un diccionario con el contenido de todos los mensajes entre estos usuarios.


#Búsqueda por texto

**Mensajes que si o si deben tener las siguientes frases**
	
La ruta para probar esta consulta sin especificar un usuario especifico vendria a ser localhost:(port)/siosi/frase donde el port es el puerto del localhost y frase viene a ser la o las frases separadas por .. que tienen que si o si estar en el mensaje, y si se desea buscar solo entre los mensajes de un usuario especifico vendria a ser localhost:(port)/siosi/frase/uid donde port y frase viene a ser lo mismo que lo ya especificado anteriormente y uid viene a ser el id del usuario dentro del cual se buscara.

Se encuentra implementada con el nombre de text_search_siosi en el archivo main.py. Esta función recibe recibe como paramatros una o más frases separadas por .. además puede recibir un id de usuario, y retorna todos los mensajes que contengan dichas frases en su contenido, que hayan sido enviados por un usuario específico(si es que este se especifico en la ruta) o de toda la base de datos en caso de no especificar el usuario.

**Mensajes que deseablemente deben tener las siguientes frases**

La ruta para probar esta consulta sin especificar un usuario especifico vendria a ser localhost:(port)/opcional/palabras donde el port es el puerto del localhost y palabras vienen a ser la o las palabras separadas por un espacio que deseablemente deben estar en el mensaje, y si se desea buscar solo entre los mensajes de un usuario especifico vendria a ser localhost:(port)/opcional/frase/uid donde port y frase viene a ser lo mismo que lo ya especificado anteriormente y uid viene a ser el id del usuario dentro del cual se buscara.

Se encuentra implementada con el nombre de text_search_opcional en el archivo main.py. Esta función recibe una o palabras separadas con un espacio y además puede recibir un id de usuario, y retorna todos los mensajes que contengan alguna de dichas palabaras en su contenido, que hayan sido enviados por un usuario específico(si es que este se especifico en la ruta) o de toda la base de datos en caso de no especificar el usuario.

**Mensajes que no deben tener las siguientes frases**

La ruta para probar esta consulta sin especificar un usuario especifico vendria a ser localhost:(port)/no/palabras donde el port es el puerto del localhost y palabras viene a ser la o las palabras separadas por un espacio que no deben estar en el mensaje, y si se desea buscar solo entre los mensajes de un usuario especifico vendria a ser localhost:(port)/no/palabras/uid donde port y frase viene a ser lo mismo que lo ya especificado anteriormente y uid viene a ser el id del usuario dentro del cual se buscara.

Se encuentra implementada con el nombre de text_search_no en el archivo main.py. Esta función recibe un string que posee palabras separadas por un espacio y además puede recibir un id de usuario, y retorna todos los mensajes que no contengan las palabras dadas en su contenido, que hayan sido enviados por un usuario específico(si es que este se especifico en la ruta) o de toda la base de datos en caso de no especificar el usuario.

**Consulta que combina las tres anteriores**

La ruta para probar esta consulta sin especificar un usuario especifico vendria a ser localhost:(port)/compuesto/frase donde el port es el puerto del localhost y frase viene a ser la o las frases separadas por dos puntos ('..') y si se desea buscar solo entre los mensajes de un usuario especifico vendria a ser localhost:(port)/compuesto/frase/uid donde port y frase viene a ser lo mismo que lo ya especificado anteriormente y uid viene a ser el id del usuario dentro del cual se buscara.

El formato en que deben estar las frases son:
+frase si es que se quiere que esa frase esté si o si <br>
-frase si es que no se quiere que esté la frase <br>
$frase si es que es opcional <br>

ejemplo:
/+hola..-buenisima..$chao

#Para probar la consulta con post

Primero debemos abrir Postman y aqui escribir la ruta localhost:(port)/messages/i/j donde i y j son los id de usuarios sender y receptant respectivamente. Posteriormente hay que escribir esto usando la opción POST, en la sección Body, opción raw y el tipo JSON(application/json) e ingresar los datos de la siguiente manera.
{
	"message": "introducir mensaje", 
	"lat": "introducir valor" ,
	"long": "introducir valor",
	"date": "introducir valor"
}

Esta funcion se encuentra implementada con el nombre de new_message en el archivo main.py, y recibe como parametros dos id de usuarios de los cuales el primero va a ser el que lo envía y el segundo el que lo recibe, además de un diccionario que posee la información que se le quiere ingresar al mensaje, y retorna un mensaje que indica el id con el que fue mandado el mensaje e ingresa el mensaje a la base de datos con un id único.

#Para probar la consulta delete

Primero debemos abrir Postman en la opcion delete y aqui escribir la ruta localhost:"port"/messages/mid donde mid viene a ser el id del mensaje que se desea borrar.

Esta funcion se encuentra implementada con el nombre de delete_message en el archivo main.py, y recibe como parametros el id de un mensaje, y retorna un mensaje que confirma la eliminación de aquel mensaje con la id seleccionada.
"# Entrega5" 
