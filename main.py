#!/usr/bin/python3
# -*- coding: utf-8 -*-

import Presentacion.CONTROLLER_UI_Principal as ui_principal
import Utils.Logger as Logger

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
