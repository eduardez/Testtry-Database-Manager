import json

PATH_TO_JSON = './res/json/preguntas.json'


# ------------------- MISC -------------------------

def buscarPreguntasRepetidas():
    json = jsonRead()
    no_repetidas = {}
    for pregunta in json['Preguntas']:
        enunciado = pregunta['enunciado']
        if not enunciado in no_repetidas:
            no_repetidas[enunciado] = pregunta
    print('Preguntas duplicadas: %s\nEliminando...' % str(len(json['Preguntas']) - len(no_repetidas)))
    json['Preguntas'] = list(no_repetidas.values())
    jsonWrite(json)


# ------------------ PLAIN TEXT FILES ----------------------
def createTXT(preguntas, nombre, poner_respuesta):
    with open(nombre+'.txt', 'w+') as f:
        j = 1
        for preg in preguntas:
            f.write(str(j) + '. ENUNCIADO: '+ preg.enunciado +'\n')
            i = 0
            for opt in preg.respuestas:
                f.write(str(i)+ opt +'\n')
                i = i+1
            if poner_respuesta:
                f.write('\n'+ preg.verdadera +'\n')

            j = j+1
            f.write('\n---------------------------------\n')


# ----------------- JSON FILES ----------------------------

def createJSONfile(pregunta):
    json = jsonRead()
    json = saveToJSON(pregunta, json)
    jsonWrite(json)


def saveToJSON(pregunta, json):
    if not isinstance(pregunta, list):
        json['Preguntas'].append(f'"enunciado":"{pregunta.enunciado}", "respuestas":3, "verdadera":"{pregunta.verdadera}"')
    else:
        for pre in pregunta:
            json['Preguntas'].append({"enunciado":pre.enunciado, "respuestas":pre.respuestas, "verdadera":pre.verdadera})
    return json


def jsonRead():
    '''
    Lee un archivo JSON el cual contiene la lista de
    canciones descargadas y lo devuelve como un objeto
    JSON.
    Si no se encuentra el archivo, el metodo creara uno
    nuevo y se llamara a si mismo para leerlo y devolverlo
    una vez creado.
    '''
    data = None
    try:
        with open(PATH_TO_JSON) as json_file:
            data = json.load(json_file)
        return data
    except Exception:
        print('\nArchivo JSON no encontrado.')
        with open(PATH_TO_JSON, 'w') as file:
            file.write('{"Preguntas": []}')
        with open(PATH_TO_JSON) as json_file:
            data = json.load(json_file)
        return data


def jsonWrite(json_data):
    '''
    Escribe en el archivo JSON los cambios efectuados
    por los orchestrators con respecto a la lista de
    canciones descargadas.
    '''
    with open(PATH_TO_JSON, 'w') as salida:
        salida.write(json.dumps(json_data, sort_keys=True, indent=4, separators=(',', ': ')))