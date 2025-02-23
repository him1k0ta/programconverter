class BaseError(Exception):
    def __init__(self, message="ошибка 1"):
        super().__init__(message)

    def __str__(self):

        return self.args[0]

class CustomError(BaseError):
    def __init__(self, message="ошибка 2"):
        super().__init__(message)

class SpecificError(CustomError):
    def __init__(self, message="ошибка 3"):
        super().__init__(message)

def error():
   # test1()
   # test2()
    test3()

def test1():
    raise BaseError("ошибка родителя")

def test2():
    raise CustomError("дочерняя ошибка")
def test3():
    raise SpecificError("дочерняя ошибка дочерней ошибки")
error()