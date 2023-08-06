class classgetter(classmethod):
    def __init__(self, func):
        super().__init__(func)

    def __get__(self, obj, objtype):
        method = super().__get__(obj, objtype)
        return method()
