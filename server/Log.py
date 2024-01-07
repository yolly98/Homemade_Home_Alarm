import os
import datetime

class Log:

    instance = None

    def __init__(self):
        self.log_file = 'log.txt'
        try:
            os.remove(self.log_file)
        except:
            pass
        

    @staticmethod
    def get_instance():
        if Log.instance is None:
            Log.instance = Log()
        return Log.instance
    
    def print(self, type, msg):
        if type == 'send':
            type = '-->'
        elif type == 'recv':
            type = '<--'
        elif type == 'success':
            type = ' + '
        elif type == 'error':
            type = ' - '
        elif type == 'cmd':
            type = ' $ '
        timestamp = datetime.datetime.now().strftime('%y/%m/%d %H:%M:%S')
        msg = f'[{timestamp}] ({type}) {msg}'
        print(msg)
        with open(self.log_file, 'a') as file:
            file.write(f'{msg}\n')