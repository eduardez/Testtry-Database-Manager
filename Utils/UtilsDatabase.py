#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import os
from hashlib import blake2b
from datetime import datetime
import traceback

DATABASE_CONFIG_FILE_NAME = 'database_info.json'
QUESTION_JSON_FILENAME = 'preguntas.json'

import Utils.Logger as Logger
logger = Logger.Logger(module='UtilsDatabase')



# -------------------- DATABASE_INFO ----------------------
def createConfigJSON(path, db_name):
    full_path = path + '/' + DATABASE_CONFIG_FILE_NAME
    with open(full_path, 'w') as file:
        file.write(newConfigTemplate(db_name))
    with open(full_path) as json_file:
        data = json.load(json_file)
    logger.info('Creating config file...')
    return data


def newConfigTemplate(db_name):
    last_update = datetime.now().strftime('%m/%d/%Y, %H:%M:%S')
    h = blake2b(digest_size=10)
    blake_string = last_update + db_name
    h.update(b'%s' % (blake_string.encode('ascii')))
    id_hash = h.hexdigest()
    template =('''{
  "database_id": "%s",
  "database_name": "%s",
  "num_preguntas": 0,
  "categorias": [
  ],
  "ultima_actualizacion": "%s"
}''' % (id_hash, db_name, last_update))
    return template


def saveConfigJSON(path, json):
    full_path = path + '/' + DATABASE_CONFIG_FILE_NAME
    jsonWrite(json, full_path)
    
    
def addNewCategory(name, path):
    full_path = path + '/' + DATABASE_CONFIG_FILE_NAME
    if createFolder(path, name):
        json = jsonRead(full_path)
        json['categorias'].append({"nombre_categoria":name, "numero_preguntas":0})
        jsonWrite(json, full_path)
        createQuestionJSON((path+'/'+name))
        return True
    else:
        return False
    
    
# ---------------- QUESTIONS ----------------
def createQuestionJSON(folder_path):
    template =('''{
    "Preguntas": []
}''')
    full_path = folder_path + '/' + QUESTION_JSON_FILENAME
    with open(full_path, 'w') as file:
        file.write(template)
    logger.success('Question JSON created.')


def appendToQuestionJSON(pregunta, path, cat):
    full_path = path + '/' + cat + '/' + QUESTION_JSON_FILENAME
    json = jsonRead(full_path)
    if not isinstance(pregunta, list):
        logger.info('Appending question to JSON')
        json['Preguntas'].append(f'"enunciado":"{pregunta.enunciado}", "respuestas":{pregunta.respuestas}, "verdadera":"{pregunta.verdadera}"')
    else:
        logger.info('Appending %d elements to JSON'%(len(pregunta)))
        for pre in pregunta:
            json['Preguntas'].append({"enunciado":pre.enunciado, "respuestas":pre.respuestas, "verdadera":pre.verdadera})
    jsonWrite(json, full_path)


def loadBBDDQuestions(cat_name, path):
    question_path = path + '/' + cat_name + '/' + QUESTION_JSON_FILENAME
    json = jsonRead(question_path)
    return json['Preguntas']
            
# ---------------- FOLDER & FOLDER STRUCTURE ----------------
def createFolder(path, name):
    folderPath = path + '/' + name
    try:
        os.mkdir(folderPath)
    except OSError:
        logger.error(f'Creation of folder {name} failed')
        traceback.print_exc()
        return False
    else:
        logger.info(f'Folder {name} created.')
        return True


# ----------------- JSON FILES ----------------------------
def jsonRead(path):
    try:
        with open(path) as json_file:
            logger.success('JSON file read successful -> ' + path)
            return json.load(json_file)
    except Exception:
        return None


def jsonWrite(json_data, path):
    with open(path, 'w') as salida:
        salida.write(json.dumps(json_data, sort_keys=True, indent=4, separators=(',', ': ')))
        logger.success('JSON file write successful -> ' + path)

# ------------------- MISC -------------------------
def buscarPreguntasRepetidas(path, cat_name):
    question_path = path + '/' + cat_name + '/' + QUESTION_JSON_FILENAME
    json = jsonRead(question_path)
    no_repetidas = {}
    for pregunta in json['Preguntas']:
        enunciado = pregunta['enunciado']
        if not enunciado in no_repetidas:
            no_repetidas[enunciado] = pregunta
    logger.info('Preguntas duplicadas: %s\nEliminando...' % str(len(json['Preguntas']) - len(no_repetidas)))
    json['Preguntas'] = list(no_repetidas.values())
    jsonWrite(json, question_path)
    

