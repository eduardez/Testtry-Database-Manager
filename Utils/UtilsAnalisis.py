
from bs4 import BeautifulSoup
import sys
from Dominio.Pregunta import Pregunta




# --------------------------- HTML CRAWLER -------------------------------
def crawlHTMLfile(path):
    soup = BeautifulSoup(open(path), "html.parser")
    preguntas = findQuestionDIV(soup)
    return preguntas
        
def findQuestionDIV(soup):
    div_list = []
    question_list = []
    for number in range(0,20):
        div_id = 'q' + str(number)
        aux1 =  soup.find("div", {"id": div_id})
        if aux1:
            div_list.append(aux1)
    for divi in div_list:
        try:
            enunciado = divi.find("div", {"class": "qtext"}).text
            opciones = procesarOpciones(divi.find("div", {"class": "answer"}))
            correcta = divi.find("div", {"class": "rightanswer"}).text
            question_list.append(Pregunta(enunciado, opciones, correcta))
        except Exception:
            pass
    return question_list
    

def procesarOpciones(divisor):
    opciones = []
    for possible in divisor.contents:
        if not possible == '\n':
            opt = str(possible.text)
            opciones.append(opt[2:])
    return opciones


