import machine
from local.file_log import FileLog

class Logger:
    def __init__(self, prefix):
        self.prefix = prefix
#        self.file_log = FileLog("logger.txt", 10000)
    
    def debug(self, *msgs):
        text = f"DEBUG: {self.prefix}{msgs}"
        self.__write_text(text)

    def error(self, *msgs):
        text = f"{self.prefix}{msgs}"
        self.__write_text(text)

    def __write_text(self, text):
#        self.file_log.write_line(text)
        print(text)



