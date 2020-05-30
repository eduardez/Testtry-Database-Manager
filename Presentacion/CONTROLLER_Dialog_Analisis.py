
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from Presentacion.UI_Files.DialogAnalisis import Ui_DialogAnalisis
import Utils.Logger as Logger
import Utils.UtilsAnalisis as utilesAnalisis
import Utils.UtilsDatabase as utilesDatabase
import sys

class DialogAnalisis(QtWidgets.QDialog, Ui_DialogAnalisis):
    def __init__(self, categorias, path, parent = None):
        super(DialogAnalisis, self).__init__(parent)
        self.logger = Logger.Logger(module='UI_Dialog_Analisis')
        self.setupUi(self)
        self.setAcceptDrops(True)
       
        self.categorias = categorias
        self.files = {}
        self.preguntas_encontradas = []
        self.db_path = path
        self.setActions()
        self.initUI()
        
        
    # --- Analisis ---
    def analizarPreguntas(self):
        preguntas = []
        self.textEdit_preguntas.clear()
        for file in self.files.values():
            preg = utilesAnalisis.crawlHTMLfile(file)
            preguntas += preg
        for p in preguntas:
            self.textEdit_preguntas.append(str(p))
        self.lbl_total_preguntas.setText(str(len(preguntas)))
        self.preguntas_encontradas = preguntas
    
    def guardarPreguntas(self):
        cat = str(self.comboBox_categorias.currentText())
        utilesDatabase.appendToQuestionJSON(self.preguntas_encontradas, self.db_path, cat)
        self.logger.info('JSON questions saved.')
        self.accept()
        
    # --- Files ---
    def appendFile(self, file):
        short_name = '...'+file[-25:]
        if (not short_name in self.files) and utilesAnalisis.isHTML(short_name):
            self.logger.info('New file added -> ' + file)
            self.files.update({short_name: file})
            self.listWidget_archivos.addItems([short_name])
    
    def deleteFile(self):
        if len(self.listWidget_archivos.selectedItems()) > 0:
            for selection in self.listWidget_archivos.selectedItems():
                file = selection.text()
                del self.files[file]
                self.logger.info('File removed -> ' + file)
            for x in self.listWidget_archivos.selectedIndexes():
                self.listWidget_archivos.takeItem(x.row())

        
    # --- UI Events ---
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [(u.toLocalFile()) for u in event.mimeData().urls()]
        for f in files:
            self.appendFile(f)
            
    # --- UI Components ---
    def setActions(self):
        self.btn_borrar_archivo.clicked.connect(lambda: self.deleteFile())
        self.btn_analizar.clicked.connect(lambda: self.analizarPreguntas())
        self.btn_guardar.clicked.connect(lambda: self.guardarPreguntas())

    def initUI(self):
        for itm in self.categorias:
            self.comboBox_categorias.addItem(itm.get('nombre_categoria'))