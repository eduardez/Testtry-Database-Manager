import termcolor
from datetime import datetime

COLOR_TYPE = {
    'ERROR': 'red',
    'INFO': 'white',
    'WARNING': 'yellow',
    'SUCCESS': 'green'
}


class Logger():
    def __init__(self, include_stack_info=True, module='root'):
        self.include_stack_info = include_stack_info
        self.colors = ('red', 'green', 'yellow', 'blue', 'magenta', 'cyan')
        self.module = module

    def start(self):
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.customPrint(f'Log iniciado {fecha}', 'INFO')

    def success(self, msg):
        self.customPrint(msg, 'SUCCESS')

    def warning(self, msg):
        self.customPrint(msg, 'WARNING')

    def error(self, msg):
        self.customPrint(msg, 'ERROR')

    def info(self, msg):
        self.customPrint(msg, 'INFO')

    def customPrint(self, msg, type):
        formatted_msg = f'[{type}]({self.module}, {datetime.now().strftime("%H:%M:%S")}): {msg}'
        colored_msg = termcolor.colored(formatted_msg, COLOR_TYPE.get(type))
        print(colored_msg)
