

class Pregunta():
    def __init__(self, enunciado, respuestas, verdadera):
        self.enunciado = enunciado
        self.respuestas = respuestas
        self.verdadera = verdadera
    
    def __str__(self):
        return(f'\n\nEnunciado: {self.enunciado} \nRespuestas: {self.respuestas} \nVerdadera: {self.verdadera}\n')