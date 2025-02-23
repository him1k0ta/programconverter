import  random
class Parents:
    def __init__(self):
        self._property = 'ЗАЩИЩЕННЫЙ АТРИБУТ'

    def papa(self):
        print('папа родитель')

    def mama(self):
        print('мама родитель')

    def uncle(self):
        print('дядя')

class Child(Parents):
    def __init__(self):
        super().__init__()

    def papa(self):
        super().papa()
        print('папа родитель')

    def mama(self):
        print('мама родитель')

    def aunt(self):
        a = random.randint(1,2)
        if a == 1:
            self.mama()
            super().mama()
        else:
            super().mama()
            self.mama()

    def babushka(self):
        print(self._property)

t = Child()

t.papa()
t.mama()
t.uncle()
t.aunt()
t.babushka()