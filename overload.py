class Main:
    def __init__(self,a,y):
        self.a = a
        self.y = y
    def __str__(self):

        return '({}, {})'.format(self.a, self.y)
    def __eq__(self, other):

        return (self.a == other.a) and (self.y == other.y)
    def __gt__(self,other):

        return (self.a > other.a) and (self.y > other.y)
    def __add__(self, other):

        return Main(self.a + other.a, self.y + other.y)

a = Main(5,2)
y = Main(2,1345)
print(a == y)
print(a + y)
print(a > y)
print(a < y)
