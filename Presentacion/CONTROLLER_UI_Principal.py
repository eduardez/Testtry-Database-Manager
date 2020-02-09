#!/usr/bin/python3
# -*- coding: utf-8 -*-

import Dominio.TesttryDB as Tdb
import Utils.Logger as Logger
from PyQt5 import QtCore, QtGui, QtWidgets

class Controller():
    def __init__(self):
        self.logger = Logger.Logger(module='VIEW_UI_Principal')

        self.necesita_guardar = False
        self.ruta = ''
        self.testtry_db_object = None

    def nuevaBBDD(self):
        path = self.fileDialog('save')
    
    
    def cargarBBDD(self):
        tmp_path = self.fileDialog('open')
        if tmp_path:
            self.logger.info('Analizando directorio.')

    def guardarBBDD(self):
        pass
    
    def addCategoria(self):
        pass
    
    
    def fileDialog(self, _type):
        if _type == 'open':
            fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","All Files (*);")
        elif _type == 'save':
            fileName, _ = QtWidgets.QFileDialog.getSaveFileName(None,"QFileDialog.getSaveFileName()","","All Files (*);")
        if fileName:
            self.logger.info('DB path: ' + str(fileName))
            return fileName
        else:
            self.logger.warning('DB path selection cancelled.')