
class Logger:
    def __init__(self, prefix):
        self.prefix = prefix
    
    def debug(self, *msgs):
        print("DEBUG: {prefix}{messages}".format(prefix = self.prefix, messages = msgs))

    def error(self, *msgs):
        print("ERROR: {prefix}{messages}".format(prefix = self.prefix, messages = msgs))




