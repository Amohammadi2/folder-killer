class Logger:

    instance = None

    def __init__(self, log_file="log.txt"):
        if Logger.instance: raise Exception("this class is singleton, use `getInstance()` method instead")
        Logger.instance = self
        self.log_file = log_file
     
    def debug(self, message): self.__log(message, "debug")
    def warning(self, message): self.__log(message, "warning")
    def error(self, message): self.__log(message, "error")
    
    def __log(self, message, level):
        log_message = "[{}] {}\n".format(level.upper(), message)
        try:
            with open(self.log_file, "a") as file:
                file.write(log_message)
        except FileNotFoundError:
            open(self.log_file, "w").close() # create file

    @staticmethod
    def getInstance(): return Logger.instance