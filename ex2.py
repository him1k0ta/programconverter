class Massivi:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"{self.x} {self.y}"

ploshad = [[Massivi(5, 6), Massivi(2, 9)], [Massivi(5, 3), Massivi(5, 4)]]

class Massivi2:
    @staticmethod
    def massiv2(x):
        if not x:
            print("массив пустой")
            return

        d3 = None
        a = input("введите атрибут (целое число): ")

        try:
            a = int(a)
        except ValueError:
            print("Ошибка: введено не целое число.")
            return

        for i in range(len(x)):
            for j in range(len(x[i])):
                if x[i][j].x == a or x[i][j].y == a:
                    d3 = x[i][j]
                    if j + 1 < len(x[i]):
                        if x[i][j].x == a and x[i][j].y < x[i][j + 1].y:
                            d3 = x[i][j]
                        elif x[i][j].y == a and x[i][j].x < x[i][j + 1].x:
                            d3 = x[i][j]

        if d3 is not None:
            print(d3)
        else:
            print('вы ввели неправильный атрибут')

Massivi2.massiv2(ploshad)