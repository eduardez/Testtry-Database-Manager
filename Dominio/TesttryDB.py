import json
from datetime import datetime
import Dominio.Pregunta as pregunta
import Utils.UtilsDatabase as utilsDatabase

class TesttyDB:
    def __init__(self):
        self.database_id = ''
        self.database_name = ''
        self.num_question = 0
        self.num_cats = 0
        self.categories = [] #array de dict [{'nombre_categoria': , 'numero_preguntas': },{}, ...]
        self.dict_questions = [] #[[cat_name], [quest1, quest2, ...]], ... }
        self.last_update = None
        self.database_path = None
        
    
    def initJSON(self, json, path):
        self.database_id = json['database_id']
        self.database_name = json['database_name']
        self.num_question = int(json['num_preguntas'])
        self.num_cats = len(json['categorias'])
        self.database_path = path
        self.parseCategories(json['categorias'])
        self.last_update = json['ultima_actualizacion']

    
    def parseCategories(self, json):
        for cat in json:
            self.categories.append(cat)
            self.dict_questions.append([cat.get('nombre_categoria'), utilsDatabase.loadBBDDQuestions(cat.get('nombre_categoria'), self.database_path)])

    def addNewCategory(self, name):
        self.categories.append({"nombre_categoria":name, "numero_preguntas":0})
        self.num_cats += 1

    def addPregunta(self, cat, pregunta):
        q_array = []
        total = 0
        if not isinstance(pregunta, list):
            q_array.append(pregunta)
            self.num_question += 1
        else:
            for pre in pregunta:
                q_array.append(pre)
            self.num_question += len(pregunta)
        for questions in self.dict_questions:
            if questions[0] == cat:
                questions[1] += q_array
                total = len(questions[1])
                break
        for cat_item in self.categories:
            cat_name = cat_item.get('nombre_categoria')
            if cat_name == cat:
                cat_item.update({"nombre_categoria":cat_name, "numero_preguntas":total})
        
    def getJSON(self):
        fecha = datetime.now().strftime("%H:%M:%S")
        num_preguntas = 0
        for cat in self.categories:
            num_preguntas += cat.get('numero_preguntas')
        template =('''{
  "database_id": "%s",
  "database_name": "%s",
  "num_preguntas": %d,
  "categorias": [
  ],
  "ultima_actualizacion": "%s"
}''' % (self.database_id, self.database_name, num_preguntas, fecha))
        json_object = json.loads(template)
        for cat in self.categories:
            json_object['categorias'].append({"nombre_categoria":cat.get('nombre_categoria'), "numero_preguntas":cat.get('numero_preguntas')})
        return json_object

    def catArrayToString(self):
        all_cats = '''
    |        Name        |   No. Questions   |
    |--------------------|-------------------|'''
        for cat in self.categories:
            categoria = cat.get("nombre_categoria")
            num_preguntas = str(cat.get("numero_preguntas"))
            if len(categoria) < 20:
                categoria += ((20-len(categoria))*' ')
            if len(num_preguntas) < 20:
                num_preguntas += ((19-len(num_preguntas))*' ')
            new_cat = f'\n    |{categoria}|{num_preguntas}|'
            all_cats += new_cat
        all_cats += '\n    |____________________|___________________|'
        return all_cats
    
    def __str__(self):
        return(f'''
------------------------
Database ID: {self.database_id}
Name: {self.database_name}
#Questions: {self.num_question}
#Categories: {self.num_cats}
Categories: {self.catArrayToString()}
Last update: {self.last_update}
               ''')