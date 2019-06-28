from flask import Flask, render_template, request, abort, json
from pymongo import MongoClient
import os
import atexit
import subprocess

# Variable que muestra las keys de los mensajes
MESSAGES_KEYS = ['message', 'lat', 'long', 'date']
USER_KEYS = ['uid', 'nombre', 'nacimiento', 'correo', 'nacionalidad']

# Se configura el uso de la base de datos en mongo
#mongod = subprocess.Popen('mongod', stdout=subprocess.DEVNULL)
#atexit.register(mongod.kill)

# Configuraciones más amigables para el uso de la base de datos

client = MongoClient('mongodb://admin:thisisapassword321@test-shard-00-00-rrldq.mongodb.net:27017,test-shard-00-01-rrldq.mongodb.net:27017,test-shard-00-02-rrldq.mongodb.net:27017/test?ssl=true&replicaSet=test-shard-0&authSource=admin&retryWrites=true&w=majority')
db = client["test"]
usuarios = db.users
mensajes = db.messages

# Se crea un índice de texto en la base de datos para poder hacer el text search
mensajes.create_index([('message', 'text')])

app = Flask(__name__)

# Modifica el encoding para que no sea ASCII el output de los json
app.config["JSON_AS_ASCII"] = False

# Función que se ejecuta al usar la ruta 'localhost:"port"/'
@app.route("/")
def home():
    """
    Retorna el mensaje 'Entrega 4 Grupo 41' 
    """
    return "<h1>Entrega 4 Grupo41</h1>"

# Función que se ejecuta al usar la ruta 'localhost:"port"/users/"uid"'
@app.route("/users/<int:uid>")
def get_user(uid):
    """
    Recibe un id de usuario que debe ser un int
    Retorna un diccionario con la información del usuario y el contenido de 
    todos sus mensajes enviados
    """
    users = list(usuarios.find({'uid' : uid}, {'_id' : 0}))
    message = list(mensajes.find({'sender': uid}, {'message' : 1, '_id' : 0}))
    return json.jsonify({'info usuario':users, 'mensajes': message})

# Función que se ejecuta al usar la ruta 'localhost:"port"/messages/mid'
@app.route("/messages/<int:mid>")
def get_message(mid):
    """
    Recibe el id de un mensaje
    Retorna un diccionario con la información del mensaje con la id entregada
    """
    message = list(mensajes.find({'mid': mid}, {'_id': 0}))
    return json.jsonify({'datos mensaje': message})

# Función que se ejecuta al usar la ruta 'localhost:"port"/twousers/uid1/uid2'
@app.route("/twousers/<int:uid1>/<int:uid2>")
def get_two_users(uid1, uid2):
    """
    Recibe dos id de usuarios
    Retorna un diccionario con el contenido de todos los mensajes en que estos 
    usuarios interactuan entre ellos
    """
    messages1 = list(mensajes.find({'sender': uid1, 'receptant': uid2},
                                    {'message' : 1, '_id': 0}))
    messages2 = list(mensajes.find({'sender': uid2, 'receptant': uid1},
                                    {'message' : 1, '_id': 0}))
    return json.jsonify({'mensajes del {0} al {1}'
                        .format(uid1, uid2): messages1,
                        'mensajes del {0} al {1}'
                        .format(uid2, uid1): messages2})

# Función que se ejecuta al usar la ruta 'localhost:"port"/frase' o
# al usar la ruta 'localhost:"port"/frase/uid'
@app.route("/siosi/<frase>", defaults={'uid': None})
@app.route("/siosi/<frase>/<int:uid>")
def text_search_siosi(frase,uid):
    """
    Recibe una o más frases separadas por .. y puede recibir un id de usuario
    Retorna todos los mensajes que contengan dichas frases en su contenido que
    hayan sido enviados por un usuario específico o de toda la base de datos en
    caso de no especificar el usuario
    """
    frase = frase.split('..')
    frase_consulta = ''
    for elemento in frase:
        frase_consulta += '"{0}"'.format(elemento)
    # Caso sin usuario especificado
    if uid == None:
        messages1 = list(mensajes.find({'$text': {'$search': frase_consulta}},
                                                 {'message': 1, '_id': 0}))
    # Caso con usuario especificado
    else:
        messages1 = list(mensajes.find({'sender': uid, '$text': 
                                       {'$search': frase_consulta}},
                                       {'message': 1, '_id': 0}))
    return json.jsonify({'mensajes': messages1})

# Función que se ejecuta al usar la ruta 'localhost:"port"/opcional' o
# al usar la ruta 'localhost:"port"/opcional/uid'
@app.route("/opcional/<frase>", defaults={'uid': None})
@app.route("/opcional/<frase>/<int:uid>")
def text_search_opcional(frase,uid):
    """
    Recibe una o palabras separadas con un espacio y puede recibir un id de 
    usuario
    Retorna todos los mensajes que contengan alguna de dichas palabaras en su
    contenido que hayan sido enviados por un usuario específico o de toda la 
    base de datos en caso de no especificar el usuario
    """
    # Caso sin usuario especificado
    if uid == None:
        messages1 = list(mensajes.find({'$text': {'$search': frase}},
                                                 {'message': 1, '_id': 0}))
    # Caso con usuario especificado
    else:
        messages1 = list(mensajes.find({'sender': uid, '$text': 
                                       {'$search': frase}},
                                       {'message': 1, '_id': 0}))
    return json.jsonify({'mensajes': messages1})


# Función que se ejecuta al usar la ruta 'localhost:"port"/no/palabras' o
# al usar la ruta 'localhost:"port"/mo/palabras/uid'
@app.route("/no/<palabras>", defaults={'uid': None})
@app.route("/no/<palabras>/<int:uid>")
def text_search_no(palabras, uid):
    """
    Recibe un string que posee palabras separadas por ' ' y puede recibir
    un id de usuario
    Retorna todos los mensajes que no contengan las palabras dadas
    """
    # Caso sin usuario especificado
    if uid == None:
        message = list(mensajes.find({'$text': {'$search': palabras}},
                                               {'message': 1, '_id': 0}))
        message_tot = list(mensajes.find({},{'message': 1, '_id': 0}))

    # Caso con usuario especificado
    else:
        message = list(mensajes.find({'$text': {'$search': palabras}, 
                                      'sender': uid},{'message': 1, '_id': 0}))
        message_tot = list(mensajes.find({'sender': uid},
                                         {'message': 1, '_id': 0}))

    # Se eliminan de la respuesta final los mensajes que poseen las palabras 
    # especificadas
    for element in message_tot:
        for bad_element in message:
            if element == bad_element:
                message_tot.remove(bad_element)
    return json.jsonify({'mensajes': message_tot})


@app.route("/compuesto/<frase>", defaults={'uid': None})
@app.route("/compuesto/<frase>/<int:uid>")
def text_search_compuesto(frase, uid):
    frases = frase.split("..")
    frases_siosi = ''
    frases_opcionales = ''
    frases_no = ''
    for elemento in frases:
        if elemento[0] == "+":
            frases_siosi += '"{0}"'.format(elemento[1:])
        elif elemento[0] == "$":
            frases_opcionales += elemento[1:] + ' '
        else:
            frases_no += elemento[1:] + ' '
    if frases_opcionales:
        frases_opcionales = frases_opcionales[0:-1]
    if frases_no:
        frases_no = frases_no[0:-1]
    if uid == None:
        if frases_siosi:
            messages = list(mensajes.find({'$text': {'$search': frases_siosi}},
                                                    {'message': 1, '_id': 0}))
        elif frases_opcionales:
            messages = list(mensajes.find({'$text': {'$search': frases_opcionales}},
                                                 {'message': 1, '_id': 0}))
        else:
            messages = list(mensajes.find({},{'message': 1, '_id': 0}))
        messages_no = list(mensajes.find({'$text': {'$search': frases_no}},
                                               {'message': 1, '_id': 0}))

    # Caso con usuario especificado
    else:
        if frases_siosi:
            messages = list(mensajes.find({'sender': uid, '$text': 
                                        {'$search': frases_siosi}},
                                        {'message': 1, '_id': 0}))
        elif frases_opcionales:
            messages = list(mensajes.find({'sender': uid, '$text': 
                                       {'$search': frases_opcionales}},
                                       {'message': 1, '_id': 0}))
        else:
            messages = list(mensajes.find({'sender': uid},
                                         {'message': 1, '_id': 0}))
        messages_no = list(mensajes.find({'$text': {'$search': frases_no}, 
                                      'sender': uid},{'message': 1, '_id': 0}))
    for element in messages:
        for bad_element in messages_no:
            if element == bad_element:
                messages.remove(bad_element)
    return json.jsonify({'mensajes': messages})
                                    



# Función que se ejecuta al usar la ruta 'localhost:"port"/messages/uid1/uid2'
# Adicionalmente se deben ingresar datos del mensaje como un diccionario
# desde Postman usando la opción Post
@app.route("/messages/<int:uid1>/<int:uid2>", methods=['POST'])
def new_message(uid1, uid2):
    """
    Recibe dos id de usuarios de los cuales el primero va a ser el que lo envía
    y el segundo el que lo recibe, además de un diccionario que posee la 
    información que se le quiere ingresar al mensaje
    Retorna un mensaje que indica el id con el que fue mandado el mensaje e 
    ingresa el mensaje a la base de datos con un id único
    """
    data = {key: request.json[key] for key in MESSAGES_KEYS}
    data['sender'] = uid1
    data['receptant'] = uid2
    # Optiene el mayor id existente para poder generar un id único
    last = list(mensajes.find({}, {'mid': 1, '_id': 0}).limit(1).sort('mid', -1))
    data['mid'] = last[0]['mid'] + 1
    
    result = mensajes.insert_one(data)
    if (result):
        message = "mensaje creado con id {}".format(data['mid'])
        success = True
    else:
        message = "No se pudo crear el mensaje"
        success = False
    return json.jsonify({'success': success, 'message': message})
    



@app.route("/create_user", methods=['POST'])
def new_user():
    data = {key: request.json[key] for key in USER_KEYS}

    result = usuarios.insert_one(data)
    if (result):
        message = "usuario creado con id {}".format(data['uid'])
        success = True
    else:
        message = "No se pudo crear el usuario"
        success = False
    return json.jsonify({'success': success, 'message': message})
    pass


# Función que se ejecuta al usar la ruta 'localhost:"port"/messages/mid'
# Recordar seleccionar la opción de delete en Postman
@app.route('/messages/<int:mid>', methods=['DELETE'])
def delete_message(mid):
    """
    Recibe el id de un mensaje
    Retorna un mensaje que confirma la eliminación de aquel con la id 
    seleccionada
    """
    mensajes.delete_one({"mid": mid})
    message = f'Mensaje con id={mid} ha sido eliminado.'
    return json.jsonify({'result': 'success', 'message': message})

# Función que se ejecuta al usar la ruta 'localhost:"port"/test'
@app.route("/test")


def test():
    """
    No recibe parametros
    Sirve para testear el servidor
    Retorna OK 
    """
    # Obtener un parámero de la URL
    param = request.args.get('name', False)
    print("URL param:", param)

    # Obtener un header
    param2 = request.headers.get('name', False)
    print("Header:", param2)

    # Obtener el body
    body = request.data
    print("Body:", body)

    return "OK"



if os.name == 'nt':
    app.run(debug = True)
