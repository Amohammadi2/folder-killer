import functools
class Logger:

    instance = None

    def __new__(cls):
        if not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, log_file="log.txt"):
        self.log_file = log_file
        self.debug = functools.partial(self.__log, "debug")
        self.warning = functools.partial(self.__log, "warning")
        self.error = functools.partial(self.__log, "error")
    
    def __log(self, level, message):
        log_message = "[{}] {}\n".format(level.upper(), message)
        with open(self.log_file, "a+") as file:
            file.write(log_message)