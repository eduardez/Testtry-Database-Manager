#!/usr/bin/python3
# -*- coding: utf-8 -*-
import Presentacion.VIEW_UI_Principal as ui_principal
import Utils.Logger as Logger

# class TesttryDatabaseShell(cmd.Cmd):
#     intro = 'Tesstry Database Manager shell. ? or Help\n'
#     prompt = '(TesttryDBM)> '

#     def do_analizar_html(self, arg):
#         try:
#             preguntas = ut_analisis.crawlHTMLfile(input('Introducir ruta:'))
#             for p in preguntas:
#                 print(p)
#         except Exception:
#             print('Archivo no encontrado.')

#     def do_eskeree(self, arg):
#         '''Método para salir del programa'''
#         print('El programa ha finalizado')
#         sys.exit(0)

if __name__ == "__main__":
    logger = Logger.Logger(module='main')
    app_info = '''
---------------------------------
    Testtry Database Manager
            v0.2.0
          @eduardez
---------------------------------
    '''
    logger.success(app_info)
    ui_principal.start()
