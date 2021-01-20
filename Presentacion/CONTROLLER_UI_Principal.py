# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtWidgets
import Utils.Logger as Logger
import Utils.UtilsDatabase as utilsDatabase
import Presentacion.CONTROLLER_Dialog_Analisis as dialogAnalisis
from Presentacion.UI_Files.UI_Principal import Ui_frm_principal
import Dominio.TesttryDB as Tdb

import sys 

class Ui_Principal(QtWidgets.QMainWindow, Ui_frm_principal):
    def __init__(self, frame, parent = None):
        super(Ui_Principal, self).__init__(parent)
        self.logger = Logger.Logger(module='CONTROLLER_UI_Principal')        
        self.necesita_guardar = False
        
        # --- App info ---
        self.testtry_database_path = ''
        self.testtry_db_object = None
        self.dict_ui_tabs = {}
        self.dict_ui_tables = {}
        self.table_header_x = ['Pregunta', 'Opciones', 'Respuesta']

        # --- Init methods ---
        self.frm_principal = frame
        self.setupUi(self.frm_principal)
        self.setValues()
        self.setActions()
        
        
    def setValues(self):
        self.lbl_testtry_icon.setStyleSheet("image: url(./Presentacion/resources/LogoBig.png);")
        # self.frm_options.setEnabled(False)
        
    def setActions(self):
        self.btn_cargar_bbdd.clicked.connect(lambda: self.cargarBBDD())
        self.btn_nueva_bbdd.clicked.connect(lambda: self.nuevaBBDD())
        self.btn_add_categoria.clicked.connect(lambda: self.addNewCategoria())
        self.btn_print_database_object.clicked.connect(lambda: self.printDBObject())
        self.btn_analizar_html.clicked.connect(lambda: self.newHTMLAnalisis())
        self.btn_guardar_bbdd.clicked.connect(lambda: self.saveBBDD())
        self.btn_clean_database.clicked.connect(lambda: self.cleanDatabase())
    
    # --- UI Methods -----
    def updateBDInfoValues(self):
        self.logger.info('Ui labels info updated.')
        self.lbl_id_db.setText(self.testtry_db_object.database_id)
        self.lbl_db_name.setText(self.testtry_db_object.database_name)
        self.lbl_numero_categorias.setText(str(self.testtry_db_object.num_cats))
        self.lbl_numero_preguntas.setText(str(self.testtry_db_object.num_question))
        self.lbl_ruta_bbdd.setText(self.testtry_database_path)
        self.clearAllTabs()
        self.loadUiTabs()    
    
    def loadUiTabs(self):
        for cat in self.testtry_db_object.categories:
            name = cat.get('nombre_categoria')
            self.addUiTab(name)
            
    def addUiTab(self, name):
        self.logger.info('Adding new tab ->' + name + '.')
        new_tab = QtWidgets.QWidget()
        new_tab.setObjectName("tab_" + name)
        self.dict_ui_tabs.update({name: new_tab})
        self.newTable(name)
        self.frm_tabs.addTab(new_tab, name)


    def clearAllTabs(self):
        self.logger.info('Cleaning all tabs.')
        self.frm_tabs.clear()
        self.dict_ui_tabs = {}
        self.dict_ui_tables = {}
        
    # --- Database Creation methods ---
    def nuevaBBDD(self):
        self.logger.info('Creating new Testtry Database...')
        path = self.fileDialog('save')
        try:
            db_name = path.split('/')
            db_name = db_name[len(db_name)-1]
            utilsDatabase.createFolder(path, '')
            utilsDatabase.createConfigJSON(path, db_name)
        except Exception as e:
            self.logger.error('Error creating database.' + str(e) + '\n')
        else:
            self.logger.success('New Testtry Database created!')
            if self.check_autoload.isChecked():
                self.loadBBDDFolder(path)

    def cargarBBDD(self):
        path = self.fileDialog('open')
        if path:
            self.loadBBDDFolder(path)
            
    def loadBBDDFolder(self, path):
        self.logger.info(f'Searching config file ({path}).')
        configfile_path = path + '/' + utilsDatabase.DATABASE_CONFIG_FILE_NAME
        try:
            json_data = utilsDatabase.jsonRead(configfile_path)
            tmp_tdb = Tdb.TesttyDB()
            tmp_tdb.initJSON(json_data, path)
            self.testtry_db_object = tmp_tdb
            self.testtry_database_path = path
            self.updateBDInfoValues()
            self.frm_options.setEnabled(True)
            self.logger.success('Database succesfully loaded.')
        except Exception as e:
            self.logger.error('Error loading Testtry database. ' + str(e) + '\n')
            
    def saveBBDD(self):
        json = self.testtry_db_object.getJSON()
        utilsDatabase.saveConfigJSON(self.testtry_database_path, json)
        
    # --- Cat methods ---    
    def addNewCategoria(self):
        name = self.inputTextDialog('Nueva categoria', 'Nombre: ', 'Creating new category: ')
        if utilsDatabase.addNewCategory(name, self.testtry_database_path):
            self.testtry_db_object.addNewCategory(name)
            self.addUiTab(name)
            self.logger.success('New category created -> ' + name)
            self.updateBDInfoValues()
        else:
            self.errorDialog('Could not create new category. Check name and/or db folder structure.')

    # --- Misc ---
    def printDBObject(self):
        self.logger.info(str(self.testtry_db_object))

    def newHTMLAnalisis(self):
        dialogo = dialogAnalisis.DialogAnalisis(categorias=self.testtry_db_object.categories, path=self.testtry_database_path)
        if dialogo.exec_():
            cat = str(dialogo.comboBox_categorias.currentText())
            preguntas = dialogo.preguntas_encontradas
            self.testtry_db_object.addPregunta(cat, preguntas)
            self.updateBDInfoValues()

    def newTable(self, name):
        tab = self.dict_ui_tabs.get(name)
        horizontalLayout_tabla = QtWidgets.QHBoxLayout(tab)
        horizontalLayout_tabla.setContentsMargins(0, 0, 0, 0)
        horizontalLayout_tabla.setObjectName("horizontalLayout_tabla_" + name)
        
        tabla = QtWidgets.QTableWidget()
        horizontalLayout_tabla.addWidget(tabla)
        tabla.setObjectName("tab_table_"+name)
        self.dict_ui_tables.update({name: tabla})
        self.logger.info('New table added to tab -> tab_table_%s ' %(name))
        
        tabla.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        tabla.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        tabla.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        tabla.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        tabla.setTextElideMode(QtCore.Qt.ElideRight)
        tabla.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        tabla.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        tabla.setShowGrid(True)
        tabla.setGridStyle(QtCore.Qt.SolidLine)
        tabla.horizontalHeader().setVisible(True)
        tabla.horizontalHeader().setCascadingSectionResizes(False)
        tabla.horizontalHeader().setMinimumSectionSize(100)
        tabla.verticalHeader().setDefaultSectionSize(44)
        tabla.verticalHeader().setMinimumSectionSize(45)
        tabla.setColumnCount(len(self.table_header_x))
        tabla.setRowCount(0)
        
        for i in range(len(self.table_header_x)):
            item = QtWidgets.QTableWidgetItem()
            item.setText(self.table_header_x[i])
            font = QtGui.QFont()
            font.setPointSize(14)
            item.setFont(font)
            tabla.setHorizontalHeaderItem(i, item)

        if self.testtry_db_object:
            for cat in self.testtry_db_object.dict_questions:
                if cat[0] == name:
                    for question in cat[1]:
                        self.addQuestionToTable(tabla, question)
        tabla.resizeColumnsToContents()

    def addQuestionToTable(self, table, question):
        num_fila = table.rowCount()
        info = [question['enunciado'], str(question['respuestas']), question['verdadera']]
        new_row = QtWidgets.QTableWidgetItem()
        new_row.setText(str(num_fila))
        table.setVerticalHeaderItem(num_fila, new_row)
        table.setRowCount(num_fila + 1)
        for x in range(len(info)):
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(info[x]))
            table.setItem(num_fila, x, item)

    def cleanDatabase(self):
        for cat in self.testtry_db_object.categories:
            self.logger.info('Cleaning database. Category: %s' %cat.get('nombre_categoria'))
            name = cat.get('nombre_categoria')
            utilsDatabase.buscarPreguntasRepetidas(self.testtry_database_path, name)
            
    # --- Dialogs ----
    def fileDialog(self, _type):
        if _type == 'open':
            file_path= QtWidgets.QFileDialog.getExistingDirectory(None,"QFileDialog.getOpenFileName()",'', QtWidgets.QFileDialog.ShowDirsOnly)
        elif _type == 'save':
            file_path, _ = QtWidgets.QFileDialog.getSaveFileName(None,"QFileDialog.getSaveFileName()","","All Files (*);")
        if file_path:
            self.logger.info('DB path: ' + str(file_path))
            return file_path
        else:
            self.logger.warning('DB path selection cancelled.')
            
    def inputTextDialog(self, title, subtitle, text_logger):
        d, okPressed = QtWidgets.QInputDialog.getText(None, title, subtitle, QtWidgets.QLineEdit.Normal, "")
        if okPressed:
            self.logger.info(text_logger + d)
            return d
        else:
            self.logger.warning(text_logger + ' -> CANCELLED' )
            
    def errorDialog(self, message):
        self.logger.error(message)
        error_dialog = QtWidgets.QErrorMessage()
        error_dialog.showMessage(message)
        
        
def start():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    frm_principal = QtWidgets.QFrame()
    ui = Ui_Principal(frm_principal)
    ui.frm_principal.show()
    sys.exit(app.exec_())