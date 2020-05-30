from Pregunta import Pregunta
import json

def getPreguntas(path):
    txt_lines = []
    with open(path) as file:
        txt_lines = file.readlines()
    txt_lines = clearText(txt_lines)
    with open('./out.txt', 'w+') as file:
        for line in txt_lines:
            file.write(line + '\n')
    arr_preguntas = []
    while txt_lines:
        enunciado = getEnunciadoSinNumero(txt_lines.pop(0))

        opt = []
        correcta = ''
        for i in range(9):
            try:
                if not isEnunciado(txt_lines[0]):
                    opt.append(txt_lines.pop(0)[3:])
            except IndexError:
                pass
        arr_preguntas.append(Pregunta(enunciado, opt, correcta))
    arr_preguntas = setCorrectas(arr_preguntas)
    return arr_preguntas


def getEnunciadoSinNumero(enun):
    enunciado = enun.split('.')
    aux = ''
    enunciado.pop(0)
    for e in enunciado:
        aux += e
    return aux


def clearText(txt_lines):
    clean = []
    for line in txt_lines:
        if line[:2] == 'a.' or line[:2] == 'b.' or line[:2] == 'c.' or line[:2] == 'd.' or line[:2] == 'e.' or isEnunciado(line):
            clean.append(line.rstrip('\n'))
        else:
            clean[len(clean)-1] += line.rstrip('\n')
    return clean


def setCorrectas(arr_preguntas):
    arr_clean = []
    for preg in arr_preguntas:
        print(preg)
        correcta = input('9. Descartar pregunta \nRespuesta correcta: (1-%d): ' % len(preg.respuestas))
        if correcta == '9':
            pass
        elif correcta == 'ur':
            return arr_clean
        else:
            preg.verdadera = preg.respuestas[int(correcta) - 1]
            arr_clean.append(preg)
    print('Añadidas %d preguntas' % len(arr_clean))
    return arr_clean


def isEnunciado(string):
    try:
        numero = string.split('.')[0]
        numero = int(numero)
        return isinstance(numero, int)
    except Exception:
        return False


def createQuestionJSON():
    template =('''{
    "Preguntas": []
}''')
    with open('./preguntas.out', 'w+') as file:
        file.write(template)
    print('Question JSON created.')


def appendToQuestionJSON(pregunta):
    json = jsonRead('./preguntas.out')
    if not isinstance(pregunta, list):
        print('Appending question to JSON')
        json['Preguntas'].append(f'"enunciado":"{pregunta.enunciado}", "respuestas":{pregunta.respuestas}, "verdadera":"{pregunta.verdadera}"')
    else:
        print('Appending %d elements to JSON'%(len(pregunta)))
        for pre in pregunta:
            json['Preguntas'].append({"enunciado":pre.enunciado, "respuestas":pre.respuestas, "verdadera":pre.verdadera})
    jsonWrite(json, './preguntas.out')


def jsonRead(path):
    try:
        with open(path) as json_file:
            print('JSON file read successful -> ' + path)
            return json.load(json_file)
    except Exception:
        return None


def jsonWrite(json_data, path):
    with open(path, 'w') as salida:
        salida.write(json.dumps(json_data, sort_keys=True, indent=4, separators=(',', ': ')))
        print('JSON file write successful -> ' + path)


if __name__ == "__main__":
    txt_path = str(input('Ruta absoluta al archivo: '))
    preguntas = getPreguntas(txt_path)
    createQuestionJSON()
    appendToQuestionJSON(preguntas)